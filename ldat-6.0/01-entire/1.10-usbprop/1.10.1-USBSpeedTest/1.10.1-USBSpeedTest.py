#! /usr/bin/env python
#coding=utf-8
## 1.10.1 USB speed test
## 1.10.1-USBSpeedTest.py


import os
import sys
import copy
import subprocess
import re
import time

reload(sys)
sys.setdefaultencoding("utf8")

g_tag = "1.10.1-USBSpeedTest"
g_currentPath = sys.path[0]
g_publicLibPath = os.environ['AUTOTEST_PUBLIC_LIB']
sys.path.append(g_publicLibPath)

from logcase import Logcase
from caseobject import CaseObject

g_log = Logcase()
caseObj = CaseObject("usbSpeedTest", g_currentPath + "/" + g_tag + ".xml")
passwd = caseObj.getPasswd()

def getCmdResult(cmd):
	process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(o, e) = process.communicate()
	return o.strip()

def get_usb_devices(protocal):
	if protocal == "2.0":
		matchSpeed = "480"
	elif protocal == "3.0":
		matchSpeed = "5000"
	else:
		return None

	partitionList = []
	cmd = "find /sys/devices/ -name 'speed' | sed -n '/usb[0-9]*\/speed/p'"
	if getCmdResult(cmd) == "":
		return None
	for speedFile in getCmdResult(cmd).split("\n"):
		cmd = "cat " + speedFile
		speed = getCmdResult(cmd)
		if speed != matchSpeed:
			continue
		dirname = os.path.dirname(speedFile)
		cmd = "find " + dirname + " -name 'sd??' | awk -F '/' '{print $NF}'"
		if getCmdResult(cmd) == "":
			continue
		for partition in getCmdResult(cmd).split("\n"):
			partitionList.append(partition)

	if len(partitionList) == 0:
		return None
	
	deviceDictTemplet = {}.fromkeys(("name", "devicenode", "fstype", "mountpoint", "total", "used", "free", "disktype", "protocal", "read/write", "size", "time", "speed"))
	device = []		# return value

	for partition in partitionList:
		cmd = "df -h | grep " + partition
		dfinfoList = getCmdResult(cmd).split(None, 5)

		if dfinfoList[4] == "100%":
			continue

		deviceDict = copy.deepcopy(deviceDictTemplet)

		deviceDict["devicenode"] = dfinfoList[0]
		deviceDict["total"] = dfinfoList[1]

		if (deviceDict["total"][-1].upper() == "G" and float(deviceDict["total"][:-1]) >= 100.0) or (deviceDict["total"][-1].upper() == "T"):
			deviceDict["disktype"] = "harddisk"
		else:
		 	deviceDict["disktype"] = "udisk"

		deviceDict["used"] = dfinfoList[2]
		deviceDict["free"] = dfinfoList[3]
		deviceDict["mountpoint"] = dfinfoList[5]
		deviceDict["protocal"] = protocal
		deviceDict["name"] = dfinfoList[5].split("/")[-1]

		cmd = "mount | grep " + deviceDict["devicenode"]
		mountinfo = getCmdResult(cmd)

		regular = "type\s(.*)\s\("
		pattern = re.compile(regular)
		patSearch = pattern.search(mountinfo)
		deviceDict["fstype"] = patSearch.group(1)

		device.append(deviceDict)

	return device

def processMountPoint(oldMountPoint):			# 处理挂载点中的() 和 空格
	newMountPoint1 = ""
	if len(oldMountPoint.split("(")) > 1:
		for subname in oldMountPoint.split("("):
			newMountPoint1 += subname + "\\" + "("
		newMountPoint1 = newMountPoint1[:-2]
	else:
		newMountPoint1 = oldMountPoint
	newMountPoint2 = ""
	if len(newMountPoint1.split(")")) > 1:
		for subname in newMountPoint1.split(")"):
			newMountPoint2 += subname + "\\" + ")"
		newMountPoint2 = newMountPoint2[:-2]
	else:
		newMountPoint2 = newMountPoint1
	newMountPoint3 = ""
	if len(newMountPoint2.split(" ")) > 1:
		for subname in newMountPoint2.split(" "):
			newMountPoint3 += subname + "\\" + " "
		newMountPoint3 = newMountPoint3[:-2]
	else:
		newMountPoint3 = newMountPoint2
	return newMountPoint3

def main():
	resultPath = g_currentPath + "/result/"
	resourcePath = g_currentPath + "/resource/"
	
	doc = caseObj.getDocumentNode()
	data_node = caseObj.getXMLNode(doc, "data", 0)
	outputFile_node = caseObj.getXMLNode(data_node, "output_file", 0)
	outputFile = caseObj.getXMLNodeValue(outputFile_node, 0)
	outputFile = resultPath + outputFile

	scriptFile = resourcePath + g_tag + ".sh"

	if not os.path.isfile(scriptFile):
		g_log.elog(g_tag, "USB speed test abort! Script file not exist.")
		print "Message from " + g_tag + ".py, USB speed test abort! Script file not exist."
		return
	else:
		cmd = "echo " + passwd + " | sudo -S chmod a+x " + scriptFile + " 2>/dev/null"
		os.system(cmd)

	if os.listdir(resultPath):
		cmd = "echo " + passwd + " | sudo -S rm -rf " + resultPath + "* 2>/dev/null"
		os.system(cmd)

	tmpFile = resultPath + "1.10.1-result~"
	
	g_log.ilog(g_tag, "usb speed test begin.")
	print "Message from " + g_tag + ".py, USB 拷贝速度测试开始\n"

	fd = open(outputFile, "w")
	ISOTIMEFORMAT = "%Y-%m-%d \t%X"
	fd.write("测试时间： \t%s\n" % time.strftime(ISOTIMEFORMAT, time.localtime()) )
	fd.write("操作系统： \t%s\n\n" % (getCmdResult("head -n 1 /etc/issue")))
	fd.write("%s \t%s \t%s \t%s \t%s \t%s \t%s \t%s \t%s \t%s \t%s \t%s \t%s\n" % ("设备名", "设备节点", "文件系统类型", "挂载点", "总容量", "已使用", "空闲", "U盘/移动硬盘", "协议", "拷贝方向", "拷贝大小", "拷贝用时", "拷贝速度"))
	fd.close()

	# name	devicenode  fstype mountpoint  total used free disktype protocal --- read/write size time speed 
	
	for protocal in ["2.0", "3.0"]:
		devices = get_usb_devices(protocal)
		#print devices
		if devices == None or len(devices) == 0:
			g_log.wlog(g_tag, "not found USB%s device" % (protocal))
			print "Message from " + g_tag + ".py, 没有找到 USB%s 存储设备\n" % (protocal)
			continue

		for device in devices:
			free = device["free"]
			if (free[-1].upper() != 'G' and free[-1].upper() != 'T') or (free[-1].upper() == 'G' and float(free[:-1]) < 5.0):
				g_log.wlog(g_tag, "USB%s device %s free space not enough 5G, remove from test list" % (protocal, device["name"]))
				print "Messga from " + g_tag + ".py, USB 设备 %s 剩余空间不足5G，从测试列表中移除\n" % (device["name"])
				devices.remove(device)
		#print devices

		# USB to HOST
		if len(devices) == 0:
			g_log.wlog(g_tag, "USB%s len(devices) == 0, can not found USB%s device for test USB%s to host" % (protocal, protocal, protocal))
			print "Message from " + g_tag + ".py, 没有找到可用的 USB%s 设备来进行USB%s 到 主机的拷贝速度测试" % (protocal, protocal)
			continue

		for device in devices:
			cmd = "echo " + passwd + " | sudo -S " + scriptFile + " " + processMountPoint(device["mountpoint"]) + " | tee " +  tmpFile
			os.system(cmd)
			processResult(device, tmpFile, outputFile)

		# USB to USB
		if len(devices) < 2:
			g_log.wlog(g_tag, "USB%s: len(devices) < 2, no enough USB%s device for test USB%s to USB%s copy speed" % (protocal, protocal, protocal, protocal))
			print "Message from " + g_tag + ".py, 没有找到足够的USB%s 设备来进行USB%s 到 USB%s的拷贝速度测试" % (protocal, protocal, protocal)
			continue

		for device in devices[::2]:
			index = devices.index(device)
			deviceFrom = device
			if index + 1 < len(devices):
				deviceTo = devices[index + 1]
			else:
			 	break
			mountPointFrom = processMountPoint(deviceFrom["mountpoint"])
			mountPointTo   = processMountPoint(deviceTo["mountpoint"])
			cmd = "echo " + passwd + " | sudo -S " + scriptFile + " " + mountPointFrom + " " + mountPointTo + " | tee " + tmpFile
			#print cmd
			os.system(cmd)
			processResult(deviceFrom, tmpFile, outputFile)

	if os.path.isfile(tmpFile):
		cmd = "echo " + passwd + " | sudo -S rm -rf " + tmpFile
		os.system(cmd)

	g_log.ilog(g_tag, "usb speed test done.")
	print "Message form " + g_tag + ".py, USB 拷贝速度测试结束"

def processResult(device, tmpFile, outputFile):
	tmpfd = open(tmpFile, "r")
	fd = open(outputFile, "a")

	direction = ""
	size = ""
	ttime = ""
	speed = ""
	
	cmd = "echo $LANG"
	cmdResult = getCmdResult(cmd)
	if cmdResult.split(".")[0] == "en_US":	#for english
		regular1 = "\((.*)\)\s\w*,\s(.*),\s(.*)\n"
	else:	# for chinese
		regular1 = "\((.*)\)\W*(\d+\.\d+\s\W{3})\W+(\d+.*)\n"
	regular2 = "bs=\d+[A-Z]\s*count=\d+"
	for (num, line) in enumerate(tmpfd):
		patter = re.compile(regular1)
		patSearch = patter.search(line)
		if patSearch != None:
			size = patSearch.group(1)
			ttime = patSearch.group(2)
			speed = patSearch.group(3)
		else:
			patter = re.compile(regular2)
			patSearch = patter.search(line)
			if patSearch != None:
				direction = line.split(" filename=")[0]
			else:
				continue
		
		if (direction != "" and size != "" and ttime != "" and speed != ""):
			fd.write("%s \t%s \t%s \t%s \t%s \t%s \t%s \t%s \t%s \t%s \t%s \t%s \t%s\n" % (device["name"], device["devicenode"], device["fstype"], device["mountpoint"], device["total"], device["used"], device["free"], device["disktype"], device["protocal"], direction, size, ttime, speed))
			direction = ""
			size = ""
			ttime = ""
			speed = ""

	tmpfd.close()
	fd.close()

if __name__ == "__main__":
	main()

