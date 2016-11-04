#! /usr/bin/env python
#coding=utf-8
## 1.6.3 copy data test
## 1.6.3-CopyDataTest.py


import os
import sys
import copy
import re
import subprocess
import time

reload(sys)
sys.setdefaultencoding("utf8")

g_tag = "1.6.3-CopyDataTest"
g_currentPath = sys.path[0]
g_publicLibPath = os.environ['AUTOTEST_PUBLIC_LIB']
sys.path.append(g_publicLibPath)

from logcase import Logcase
from caseobject import CaseObject
from screenshot import Screenshot

g_log = Logcase()
caseObj = CaseObject(g_tag, g_currentPath + "/" + g_tag + ".xml")
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
		g_log.elog(g_tag, "Copy data test abort! Script file not exist.")
		print "Message from " + g_tag + ".py, Copy data test abort! Script file not exist."
		return
	else:
		cmd = "echo " + passwd + " | sudo -S chmod a+x " + scriptFile + " 2>/dev/null"
		os.system(cmd)

	if os.listdir(resultPath):
		cmd = "echo " + passwd + " | sudo -S rm -rf " + resultPath + "* 2>/dev/null"
		os.system(cmd)
	
	g_log.ilog(g_tag, "`Copy data test begin.")
	print "Message from " + g_tag + ".py, 拷贝数据测试开始\n"

	fd = open(outputFile, "w")
	ISOTIMEFORMAT = "%Y-%m-%d \t%X"
	fd.write("测试时间： \t%s\n" % time.strftime(ISOTIMEFORMAT, time.localtime()) )
	fd.write("操作系统： \t%s\n\n" % (getCmdResult("head -n 1 /etc/issue")))
	fd.write("%s \t%s \t%s \t%s \t%s \t%s \t%s \t%s \t%s \t%s \t%s \t%s\n" % ("设备名", "设备节点", "文件系统类型", "挂载点", "总容量", "已使用", "空闲", "U盘/移动硬盘", "协议", "原始文件MD5", "拷贝来的文件MD5", "是否正常"))
	fd.close()

	# name	devicenode  fstype mountpoint  total used free disktype protocal --- md5 md5 ok/failed

	harddisk = None
	udisk    = None
	for protocal in ["2.0", "3.0"]:
		devices = get_usb_devices(protocal)

		if devices == None or len(devices) == 0:
			continue

		for device in devices:
			free = device["free"]
			if (free[-1].upper() != 'G' and free[-1].upper() != 'T') or (free[-1].upper() == 'G' and float(free[:-1]) < 5.0):
				g_log.wlog(g_tag, "USB%s device %s free space not enough 5G, remove from test list" % (protocal, device["name"]))
				print "Messga from " + g_tag + ".py, USB 设备 %s 剩余空间不足5G，从测试列表中移除\n" % (device["name"])
				devices.remove(device)

		if len(devices) == 0:
			continue

		for device in devices:
			if device["disktype"] == "harddisk":
				harddisk = device
			if device["disktype"] == "udisk":
				udisk = device

	if harddisk != None:
		work(harddisk, scriptFile, resultPath, outputFile)
	else:
		g_log.wlog(g_tag, "can not found USB harddisk for copy data test")
		print "Message from " + g_tag + ".py, 没有找到移动硬盘来进行拷贝数据测试\n"

	if udisk != None:
		work(udisk, scriptFile, resultPath, outputFile)
	else:
		g_log.wlog(g_tag, "can not found udisk for copy data test")
		print "Message from " + g_tag + ".py, 没有找到U盘来进行拷贝数据测试\n"

	g_log.ilog(g_tag, "`Copy data test done.")
	print "Message form " + g_tag + ".py, USB 拷贝速度测试结束"
	return

def work(device, scriptFile, resultPath, outputFile):
	for datasize in ["500M", "1G", "2G", "5G"]:
		cmd = "echo " + passwd + " | sudo -S " + scriptFile + " add " + processMountPoint(device["mountpoint"]) + " " + datasize
		os.system(cmd)

		if os.path.isfile(device["mountpoint"] + "/copy_data_test_file_" + datasize):
			print "就绪"
			cmd = "md5sum " + processMountPoint(device["mountpoint"]) + "/copy_data_test_file_" + datasize + " | awk '{print $1}'"
			usbfilemd5 = getCmdResult(cmd)

			print "拷贝..."
			cmd = "cp " + processMountPoint(device["mountpoint"]) + "/copy_data_test_file_" + datasize + " " + resultPath
			os.system(cmd)

			cmd = "md5sum " + resultPath + "copy_data_test_file_" + datasize + " | awk '{print $1}'"
			diskfilemd5 = getCmdResult(cmd)

			fd = open(outputFile, "a")
			fd.write("%s \t%s \t%s \t%s \t%s \t%s \t%s \t%s \t%s \t%s \t%s \t%s\n" % (device["name"], device["devicenode"], device["fstype"], device["mountpoint"], device["total"], device["used"], device["free"], device["disktype"], device["protocal"], usbfilemd5, diskfilemd5, "ok" if usbfilemd5 == diskfilemd5 else "failed"))
			fd.close()

			cmd = "echo " + passwd + " | sudo -S " + scriptFile + " rm " + processMountPoint(device["mountpoint"]) + " " + datasize
			os.system(cmd)
			cmd = "echo " + passwd + " | sudo -S rm -rf " + resultPath + "copy_data_test_file_" + datasize + " 2>/dev/null"
			os.system(cmd)
		else:
			g_log.wlog(g_tag, "prepare %s data failed" % datasize)
			print "Message from " + g_tag + ".py, 数据准备失败\n"

	g_sst = Screenshot()
	g_sst.scrprint(g_tag, '1.6.3-screen_', g_currentPath)
	fd = open(outputFile, "a")
	fd.write("\nscreenshot目录有屏幕截图\n")
	fd.close()


if __name__ == "__main__":
	main()

