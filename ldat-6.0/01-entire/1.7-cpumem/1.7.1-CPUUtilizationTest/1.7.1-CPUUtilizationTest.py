#! /usr/bin/env python
#coding=utf-8
# 1.7.1 CPU utilization Test
# 1.7.1-cpu_utilization_test.py

import os
import sys
import subprocess
import time
from ldtp import *

reload(sys)
sys.setdefaultencoding("utf8")

g_tag = "1.7.1-CPUUtilizationTest"
g_currentPath = sys.path[0]
g_publicLibPath = os.environ['AUTOTEST_PUBLIC_LIB']
g_autotestDIR = os.environ['AUTOTEST_DIR']
sys.path.append(g_publicLibPath)

from logcase import Logcase
from caseobject import CaseObject
from screenshot import Screenshot

g_log = Logcase()
cpuUtilizationTestObj = CaseObject("cpuUtilizationTest", g_currentPath + "/" + g_tag + ".xml")

passwd = cpuUtilizationTestObj.getPasswd()
g_os = cpuUtilizationTestObj.getOSName()

def getCmdResult(cmd):
	process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(o, e) = process.communicate()
	return o.strip()

#------------------------------- firefox -----------------------------
def openWebsite(url):
	cmd = "firefox --new-window " + url + " >/dev/null 2>&1 &"
	if not os.system(cmd):
		time.sleep(5)
		return True
	else:
		return False
		
def closeFirefox():
	for i in range(10):
		if guiexist("*Firefox*"):
			closewindow("*Firefox*")
			time.sleep(1)
			if guiexist("*dlg*"):
				if g_os == "kylin":
					keypress("<enter>")
					keyrelease("<enter>")
				else:
					keypress("<alt>")
					keypress("<q>")
					keyrelease("<alt>")
					keyrelease("<q>")
		else:
			break
	
	cmd = "echo " + passwd + " | sudo -S killall firefox 2>/dev/null"
	os.system(cmd)
#-------------------------- end firefox ------------------------------

#----------------------------- WPS file -----------------------------
def openWPS(filename):
	suffix = filename.split("/")[-1].split(".")[-1]
	cmd = "which wps"
	process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(o, e) = process.communicate()
	if (o.strip() != "" and o.strip() != None):			# 安装了wps
		if suffix == "wps" or suffix == "doc" or suffix == "docx":
			cmd = "wps " + filename + " >/dev/null 2>&1 &"
		elif suffix == "et" or suffix == "xlsx" or suffix == "xls":
			cmd = "et " + filename + " >/dev/null 2>&1 &"
		elif suffix == "dps" or suffix == "ppt":
			cmd = "wpp " + filename + " >/dev/null 2>&1 &"
		else:
			return False
		if not os.system(cmd):
			time.sleep(3)
			i = 0
			while (guiexist("dlg*", "btn*")):
				keypress("<enter>")
				keyrelease("<enter>")
				time.sleep(1)
				i = i + 1
				if i > 3:
					break
			time.sleep(1)
			return True
		else:
			return False
	else:																		# 未安装wps
		cmd = "soffice -norestore " + filename + " >/dev/null 2>&1 &"
		if not os.system(cmd):
			time.sleep(1)
			while (guiexist("dlg*", "btn*")):
				if activatewindow("dlg*") == 0:
					break
				else:
					time.sleep(1)
					keypress("<enter>")
					keyrelease("<enter>")
					time.sleep(2)
			time.sleep(5)
			return True
		else:
			while (guiexist("dlg*", "btn*")):
				activatewindow("dlg*")
				time.sleep(1)
				keypress("<enter>")
				keyrelease("<enter>")
				time.sleep(1)
			return False

def closeWPS():
	cmd = "which wps"
	process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(o, e) = process.communicate()
	if (o.strip() != "" and o.strip() != None):
		processList = ["wps", "et", "wpp"]
		for processName in processList:
			cmd = "echo " + passwd + " | sudo -S killall " + processName + " 2>/dev/null"
			os.system(cmd)
	else:
		cmd = "echo " + passwd + " | sudo -S killall soffice 2>/dev/null"
		os.system(cmd)
#-----------------------------end wps file-----------------------------

#---------------------------- multimedia ------------------------------
def openMultimedia(filename):
	if g_os == "kylin":
		cmd = "smplayer " + filename + " >/dev/null 2>&1 &"
		if not os.system(cmd):
			time.sleep(5)
			activatewindow("*" + filename.split("/")[-1].strip() + "*")
			time.sleep(5)
			return True
		else:
			return False
	suffix = filename.split("/")[-1].split(".")[-1].strip()
	if suffix == "mp3" or suffix == "wav" or suffix == "ogg":	#audio
		if g_os == "isoft":
			cmd = "audacious " + filename + " >/dev/null 2>&1 &"
		elif g_os == "cos":
			cmd = "rhythmbox " + filename + " >/dev/null 2>&1 &"
		else:
			cmd = "rhythmbox " + filename + " >/dev/null 2>&1 &"
		if not os.system(cmd):
			time.sleep(5)
			activatewindow("*" + filename.split("/")[-1].strip() + "*")
			time.sleep(5)
			return True
		else:
			return False
	elif suffix == "wmv" or suffix == "flv" or suffix == "mkv" or suffix == "mp4" or suffix == "mpg" or suffix == "vob" or suffix == "rmvb":
		cmd = "totem --play " + filename + " >/dev/null 2>&1 &"
		if not os.system(cmd):
			time.sleep(5)
			activatewindow("*" + filename.split("/")[-1].strip() + "*")
			time.sleep(5)
			return True
		else:
			return False
	else:
		return False
		
def closeMultimedia():
	if g_os == "kylin":
		cmd = "ps -ef | grep smplayer | grep -v grep | awk '{print $2}'"
		process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		(o, e) = process.communicate()
		for processID in o.split("\n"):
			cmd = "echo  " + passwd + " | sudo -S kill -9 " + processID + " >/dev/null 2>&1"
			os.system(cmd)
		return
	cmd = "totem --quit >/dev/null 2>&1"
	os.system(cmd)
	if g_os == "isoft":
		cmd = "ps -ef | grep audacious | grep -v grep | awk '{print $2}'"
	elif g_os == "cos":
		cmd = "ps -ef | grep rhythmbox | grep -v grep | awk '{print $2}'"
	else:
		cmd = "ps -ef | grep rhythmbox | grep -v grep | awk '{print $2}'"
	process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(o, e) = process.communicate()
	for processID in o.split("\n"):
		cmd = "echo " + passwd + " | sudo -S kill -9 " + processID + " >/dev/null 2>&1"
		os.system(cmd)
#--------------------- end multimedia -------------------------------

#---------------------------- directory -----------------------------	
def openDir(path):
	if g_os == "cos":
		cmd = "nemo " + path + " &"
	elif g_os == "isoft":
		cmd = "nemo " + path + " &"
	elif g_os == "kylin":
		cmd = "caja " + path
	else:
		cmd = "nautilus " + path
	if not os.system(cmd):
		return True
	else:
		return False

def closeDir(path):
	if not (path.split("/")[-1].strip() == None or path.split("/")[-1].strip() == ""):
		closewindow(path.split("/")[-1].strip())
#------------------------- end directory -----------------------------

def processFilename(oldFilename):			# 处理文件名中的() 和 空格
	newFilename1 = ""
	if len(oldFilename.split("(")) > 1:
		for subname in oldFilename.split("("):
			newFilename1 += subname + "\\" + "("
		newFilename1 = newFilename1[:-2]
	else:
		newFilename1 = oldFilename
	newFilename2 = ""
	if len(newFilename1.split(")")) > 1:
		for subname in newFilename1.split(")"):
			newFilename2 += subname + "\\" + ")"
		newFilename2 = newFilename2[:-2]
	else:
		newFilename2 = newFilename1
	newFilename3 = ""
	if len(newFilename2.split(" ")) > 1:
		for subname in newFilename2.split(" "):
			newFilename3 += subname + "\\" + " "
		newFilename3 = newFilename3[:-2]
	else:
		newFilename3 = newFilename2
	return newFilename3

def installPlugin():
	if  g_os == "cos":
		cmd = "dpkg -l | grep gstreamer1.0-plugins-ugly | awk '{print $1}'"
		if getCmdResult(cmd) != 'ii':
			scriptFilePath = g_autotestDIR + "/tools/build116a-codec-debs"
			if os.path.exists(scriptFilePath):
				os.chdir(scriptFilePath)
				scriptFile = "./install.sh"
				if os.path.isfile(scriptFile):
					cmd = "echo " + passwd + " | sudo -S chmod a+x " + scriptFile + " 2>/dev/null"
					os.system(cmd)
					cmd = "echo " + passwd + " | sudo -S " + scriptFile
					os.system(cmd)
				else:
					g_log.wlog(g_tag, "`install media plugin failed'")
				os.chdir(g_currentPath)
			else:
				g_log.wlog(g_tag, "`install media plugin failed'")

def main():
	iWebSite = 10
	iWPSFile = 10
	iMultimediaFile = 10
	iDirectory = 10

	resultPath = g_currentPath + "/result/"
	screenshotPath = g_currentPath + "/screenshot/"
	if os.listdir(resultPath):
		cmd = "echo " + passwd + " | sudo -S rm -rf " + resultPath + "* 2>/dev/null"
		os.system(cmd)
	if os.listdir(screenshotPath):
		cmd = "echo " + passwd + " | sudo -S rm -rf " + screenshotPath + "* 2>/dev/null"
		os.system(cmd)

	g_log.ilog(g_tag, "CPU utilization test begin.")
	print "Message from " + g_tag + ".py, CPU utilization testting..."

	doc = cpuUtilizationTestObj.getDocumentNode()
	data_node = cpuUtilizationTestObj.getXMLNode(doc, "data", 0)
	
	resourcePath = g_currentPath + "/resource/"

	closeFirefox()

	installPlugin()
	
	for i in range(0, 10):
		# Open URL
		url_node = cpuUtilizationTestObj.getXMLNode(data_node, "url", i)
	 	url = cpuUtilizationTestObj.getXMLNodeValue(url_node, 0)
		if not openWebsite(url):
			g_log.wlog(g_tag, "Can not open url " + url)
			print "Message from " + g_tag + ".py, Can not open url " + url
			iWebSite = iWebSite - 1
			
		# Open wps file
		wps_file_node = cpuUtilizationTestObj.getXMLNode(data_node, "wps_file", i)
		wps_file = cpuUtilizationTestObj.getXMLNodeValue(wps_file_node, 0)
		if os.path.basename(wps_file) == wps_file:
			wps_file = resourcePath + wps_file
		if not os.path.isfile(os.path.expanduser(wps_file)):
			g_log.wlog(g_tag, "Pls. check, wps file %s in config file isn't exist." % (wps_file))
			print "Message from " + g_tag + ".py, wps file %s in config file isn't exist." % wps_file
			iWPSFile = iWPSFile - 1
		elif not openWPS(processFilename(wps_file)):
			g_log.wlog(g_tag, "Can not open wps file " + wps_file)
			print "Message from " + g_tag + ".py, Can not open wps file " + wps_file
			iWPSFile = iWPSFile - 1
		
		# Open multimedia file
		try:
			multimedia_file_node = cpuUtilizationTestObj.getXMLNode(data_node, "multimedia_file", i)
			multimedia_file = cpuUtilizationTestObj.getXMLNodeValue(multimedia_file_node, 0)
		except:
			multimedia_file = None
		if multimedia_file != None:
			if os.path.basename(multimedia_file) == multimedia_file:
				multimedia_file = resourcePath + multimedia_file
			if not os.path.isfile(os.path.expanduser(multimedia_file)):
				g_log.wlog(g_tag, "Pls. check, multimedia file %s in config file isn't exist." % multimedia_file)
				print "Message from " + g_tag + ".py, multimedia_file %s in config file isn't exist." % multimedia_file
				iMultimediaFile = iMultimediaFile - 1
			elif not openMultimedia(processFilename(multimedia_file)):
				g_log.wlog(g_tag, "Can not open multimedia file " + multimedia_file)
				print "Message from " + g_tag + ".py, Can not open multimedia file " + multimedia_file
				iMultimediaFile = iMultimediaFile - 1
		else:
				iMultimediaFile = iMultimediaFile - 1

		# Open directory
		directory_node = cpuUtilizationTestObj.getXMLNode(data_node, "directory", i)
		directory = cpuUtilizationTestObj.getXMLNodeValue(directory_node, 0)
		if not openDir(directory):
			g_log.wlog(g_tag, "Can not open directory " + directory)
			print "Message from " + g_tag + ".py, Can not open directory " + directory
			iDirectory = iDirectory - 1

			
	outputFile_node = cpuUtilizationTestObj.getXMLNode(data_node, "output_file", 0)
	outputFile = cpuUtilizationTestObj.getXMLNodeValue(outputFile_node, 0)
	outputFile = resultPath + outputFile
	pFile = open(outputFile, "w")
	pFile.write("成功打开 %d 个网站首页, %d 个WPS文件, %d 个音视频文件 和 %d 个目录。\n"%(iWebSite, iWPSFile, iMultimediaFile, iDirectory))
	pFile.write("screenshot目录下有屏幕截图信息。\n")
	pFile.write("下次测试结果将会被覆盖，如果有需要，请保存好结果。\n\n")
	pFile.close()
	time.sleep(3)
	cmd = "top -b -n 1 | tee -a " + outputFile
	os.system(cmd)
	cmd = "sed -n '/^%Cpu/p' " + outputFile + " | awk '{print $8}'"
	cpuIdle = getCmdResult(cmd)
	cpuUsed = str(100.0 - float(cpuIdle))
	cmd = "sed -i '1a\从top命令的输出可以看出CPU使用率：%s%%，空闲：%s%%' " + outputFile
	os.system(cmd % (cpuUsed, cpuIdle))
	
	shotObj = Screenshot()
	shotObj.scrprint(g_tag, "screen", g_currentPath)
	
	closeWPS()
	closeMultimedia()
	for i in range(0, 10):
		directory_node = cpuUtilizationTestObj.getXMLNode(data_node, "directory", i)
		directory = cpuUtilizationTestObj.getXMLNodeValue(directory_node, 0)
		closeDir(directory)
	closeFirefox()
	
	g_log.ilog(g_tag, "CPU utilization test done. Result file: " + outputFile)	
	print "Message from " + g_tag + ".py, CPU utilization test done."
	
	return

if (__name__ == "__main__"):
	main()

