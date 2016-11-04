#! /usr/bin/env python
# coding=utf-8
## 1.5.1 cdrom read capacity
## 1.5.1-readCapacity.py

import os
import sys
import subprocess
import re
import time


reload(sys)
sys.setdefaultencoding("utf8")

g_tag = "1.5.1-readCapacity"
g_currentPath = sys.path[0]
g_publicLibPath = os.environ['AUTOTEST_PUBLIC_LIB']
sys.path.append(g_publicLibPath)

from logcase    import Logcase
from caseobject import CaseObject

g_log = Logcase()
readCapacityObj = CaseObject("usbSpeedTest", g_currentPath + "/" + g_tag + ".xml")
g_passwd = readCapacityObj.getPasswd()
g_resourcePath = g_currentPath + "/resource/"
g_resultPath   = g_currentPath + "/result/"

g_CD1xSpeed = 150
g_DVD1xSpeed = 1350

g_devName   = ""
g_dataSize  = ""
g_bs = ""
g_count = ""

def getCmdResult(cmd):
	process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(o, e) = process.communicate()
	return o.strip()

def setBsAndCount(configDataSize):
	global g_dataSize
	global g_bs
	global g_count
	
	cmd = "df -h | grep " + g_devName + " | awk '{print $3}'"	# 已用
	mediaTotalSize = getCmdResult(cmd)
	if mediaTotalSize == "0":
		g_log.wlog(g_tag, "CD/DVD is empty.")
		print "\n光盘中没有数据，无法进行倍速测试"
		return False

	# 获取光盘数据总容量大小，单位：KB
	unit = mediaTotalSize[-1]
	if unit == 'G' or unit == 'g':
		totalNumerical = float(mediaTotalSize[:-1]) * 1024 * 1024
	elif unit == 'M' or unit == 'm':
		totalNumerical = float(mediaTotalSize[:-1]) * 1024
	elif unit == 'K' or unit == 'k':
		totalNumerical = float(mediaTotalSize[:-1])
	else:
		g_log.elog(g_tag, "Get CD/DVD total size error!")
		print "\n获取光盘数据容量出错"
		return False
	
	# 获取配置数据大小，单位：KB
	unit = configDataSize[-1]
	if unit == 'G' or unit == 'g':
		configNumerical = float(configDataSize[:-1]) * 1024 * 1024
	elif unit == 'M' or unit == 'm':
		configNumerical = float(configDataSize[:-1]) * 1024
	elif unit == 'K' or unit == 'k':
		configNumerical = float(configDataSize[:-1])
	else:
		if configDataSize == "0":
			configNumerical = 0
		else:
			g_log.wlog(g_tag, "Configure copy data size error. Pls. check! Can't parse %s" % (configDataSize))
			print "\n配置文件有误，请检查: 无法解析: %s" % (configDataSize)
			return False
		
	if configNumerical > totalNumerical:
		print "\n光盘中数据大小不足%s，使用光盘总数据容量进行测试。" % (configDataSize)
		g_dataSize = mediaTotalSize
	elif configNumerical == 0:
		g_dataSize = mediaTotalSize
	else:
		g_dataSize = configDataSize

	if g_dataSize[-1] == "G" or g_dataSize[-1] == "g":
		g_dataSize = str(int(float(g_dataSize[:-1]) * 1024)) + "M"
		g_bs = "1M"
		g_count = str(int(float(g_dataSize[:-1])))
	elif g_dataSize[-1] == "M" or g_dataSize[-1] == "m":
		g_dataSize = str(int(g_dataSize[:-1])) + "M"
		g_bs = "1M"
		g_count = str(int(g_dataSize[:-1]))
	elif g_dataSize[-1] == "K" or g_dataSize == "k":
		g_dataSize = str(int(g_dataSize[:-1])) + "K"
		g_bs = "1K"
		g_count = str(int(g_dataSize[:-1]))
	else:
		g_log.elog(g_tag, "Get CD/DVD total size error!")
		print "\n获取光盘数据容量出错"
		return False

	return True

def main():
	global g_devName

	ISOTIMEFORMAT = "%Y-%m-%d %X"
	
	doc = readCapacityObj.getDocumentNode()
	data_node = readCapacityObj.getXMLNode(doc, "data", 0)
	outputFile_node = readCapacityObj.getXMLNode(data_node, "output_file", 0)
	outputFile = readCapacityObj.getXMLNodeValue(outputFile_node, 0)
	outputFile = g_resultPath + outputFile			#outputFile

	if os.listdir(g_resultPath):
		cmd = "echo " + g_passwd + " | sudo -S rm -rf " + g_resultPath + "* 2>/dev/null"
		os.system(cmd)

	scriptFile = g_resourcePath + g_tag + ".sh"

	if not os.path.isfile(scriptFile):
		g_log.elog(g_tag, "Can not found Script file.")
		print "\nMessage from " + g_tag + ".py, Script file not exist.\n"
		return
	else:
		cmd = "echo " + g_passwd + " | sudo -S chmod a+x " + scriptFile + " >/dev/null"
		os.system(cmd)

	cmd = "mount | grep iso9660 | awk '{print $1}' | tail -n 1"
	g_devName = getCmdResult(cmd)
	if g_devName == "":
		g_log.elog(g_tag, "Insert a CD or DVD first.")
		print "\nMessage from " + g_tag + ".py, Insert a CD or DVD first.\n"
		cmd = "echo \"没有插入光盘\" >" + outputFile
		os.system(cmd)
		return

	g_log.ilog(g_tag, "CD-ROM driver read capacity test begin.")
	print "\nMessage from " + g_tag + ".py, CD-ROM driver read capacity test begin.\n"

	data_size_node  = readCapacityObj.getXMLNode(data_node, "data_size", 0)
	media_type_node = readCapacityObj.getXMLNode(data_node, "media_type", 0)

	configMediaType = readCapacityObj.getXMLNodeValue(media_type_node, 0)

	fd = open(outputFile, "a")
	fd.write("测试时间 %s\n" % (time.strftime(ISOTIMEFORMAT, time.localtime())))
	cmd = "head -n 1 /etc/issue"
	fd.write(getCmdResult(cmd))
	fd.write("\n\n")
	fd.close()
	
	for configDataSize in readCapacityObj.getXMLNodeValue(data_size_node, 0).split(","):
		configDataSize = configDataSize.strip()
		
		if not setBsAndCount(configDataSize):
			continue
		
		dropCache = "echo " + g_passwd + " | sudo -S " + scriptFile + " >/dev/null"
		os.system(dropCache)
	
		print "\n正在从%s:文件系统%s拷贝%s数据到系统" % (configMediaType, g_devName, g_dataSize)

		cmd = "dd if=" + g_devName + " of=/dev/null bs=" + g_bs + " count=" + g_count + " 2>&1 | tee -a " + outputFile
		print "bs =", g_bs
		print "count =", g_count
		#print "cmd =", cmd
		os.system(cmd)

		os.system(dropCache)

		cmd = "tail -n 1 " + outputFile
		line = getCmdResult(cmd)

		fd = open(outputFile, "a")
	
		cmd = "echo $LANG"
		lang = getCmdResult(cmd)
		if lang.split(".")[0] == "en_US":	#for english
			regular = "\((.*)\)\s\w*,\s(.*),\s(.*)"
		else:					# for chinese
			regular = "\((.*)\)\W*(\d+\.\d+\s\W{3})\W+(\d+.*)"
		patter = re.compile(regular)
		patSearch = patter.search(line)
		if patSearch != None:
			roughSpeed = patSearch.group(3)
			numerical = roughSpeed.split(" ")[0]
			unit = roughSpeed.split(" ")[1].split("/")[0]
			if unit == "GB" or unit == "gB":
				numericalInKB = float(numerical) * 1024 * 1024
			elif unit == "MB" or unit == "mB":
				numericalInKB = float(numerical) * 1024
			else:
				numericalInKB = float(numerical)
		
			if configMediaType == "CD":
				speed = numericalInKB / g_CD1xSpeed
				fd.write("从CD光盘读取数据的倍速为：%f\n" % (speed))
			elif configMediaType == "DVD":
				speed = numericalInKB / g_DVD1xSpeed
				fd.write("从DVD光盘读取数据的倍速为：%f\n" % (speed))
			else:
				fd.write("无法根据媒体介质类型%s计算倍数\n" % (configMediaType))
		else:
			fd.write("计算倍数时出错，没有提取出速度，请手动计算\n")

		fd.write("\n注意：下次测试结果会被覆盖，如果有需要，请保存好结果\n")
		fd.close()

	g_log.ilog(g_tag, "CD-ROM driver read capacity test done.")
	print "\nMessage form " + g_tag + ".py, CD-ROM driver read capacity test done.\n"

if __name__ == "__main__":
	main()

