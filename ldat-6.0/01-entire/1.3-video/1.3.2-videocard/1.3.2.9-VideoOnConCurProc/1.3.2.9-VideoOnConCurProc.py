#coding=utf-8
#! /usr/bin/env python
# 1.3.2.9 Video on Concurrent Processing
# 1.3.2.9-VideoOnConCurProc.py

import os
import sys
import subprocess
import time
from ldtp import *

reload(sys)
sys.setdefaultencoding("utf8")

g_tag = "1.3.2.9-VideoOnConCurProc"
g_currentPath = sys.path[0]
#print "g_currentPath =", g_currentPath
#os.system("pwd")
g_publicLibPath = os.environ['AUTOTEST_PUBLIC_LIB']
sys.path.append(g_publicLibPath)

from logcase import Logcase
from caseobject import CaseObject
from screenshot import Screenshot
import threading

g_log = Logcase()
caseObj = CaseObject(g_tag, g_currentPath + "/" + g_tag + ".xml")

passwd = caseObj.getPasswd()
osname = caseObj.getOSName()

g_resourcePath = g_currentPath + "/resource/"
g_resultPath = g_currentPath + "/result/"

ALLOW_LOST_PER_SEC = 10

def getCmdResult(cmd):
	process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(o, e) = process.communicate()
	return o.strip()


def openWPS(filename):
	suffix = filename.split("/")[-1].split(".")[-1]
	cmd = "which wps"
	process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(o, e) = process.communicate()
	if (o.strip() != "" and o.strip() != None):			# 安装了wps
		if not (cmp(suffix, "wps") and cmp(suffix, "doc") and cmp(suffix, "docx")):
			cmd = "wps " + filename + " >/dev/null 2>&1 &"
		elif not (cmp(suffix, "et") and cmp(suffix, "xlsx") and cmp(suffix, "xls")):
			cmd = "et " + filename + " >/dev/null 2>&1 &"
		elif not (cmp(suffix, "dps") and cmp(suffix, "ppt")):
			cmd = "wpp " + filename + " >/dev/null 2>&1 &"
		else:
			return False
		if not os.system(cmd):
			time.sleep(1)
			i = 0
			while (guiexist("dlg*", "btn*")):
				if activatewindow("dlg*") == 0:
					break
				else:
					time.sleep(1)
					keypress("<enter>")
					keyrelease("<enter>")
					time.sleep(1)
					i = i + 1
					if i > 3:
						break
			time.sleep(2)
			return True
		else:
			return False
	else:																		# 未安装wps
		cmd = "soffice -norestore " + filename + " >/dev/null 2>&1 &"
		if not os.system(cmd):
			time.sleep(1)
			while (guiexist("*dlg*", "*btn*")):
				keypress("<enter>")
				keyrelease("<enter>")
				time.sleep(2)
			time.sleep(5)
			return True
		else:
			while (guiexist("*dlg*", "*btn*")):
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
			cmd = "ps -ef | grep /opt/kingsoft/wps-office/office6/" + processName + " | grep -v grep | awk '{print $2}'"
			process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			(o, e) = process.communicate()
			for processID in o.split("\n"):
				cmd = "echo " + passwd + " | sudo -S kill -9 " + processID + " >/dev/null 2>&1"
				os.system(cmd)
	else:
		cmd = "ps -ef | grep soffice | grep -v grep | awk '{print $2}'"
		process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		(o, e) = process.communicate()
		for processID in o.split("\n"):
			cmd = "echo " + passwd + " | sudo -S kill -9 " + processID + " >/dev/null 2>&1"
			os.system(cmd)

class videoer(threading.Thread):
	def __init__(self, videoName, outputFile):
		threading.Thread.__init__(self)
		self.videoname = videoName
		self.outputfile = outputFile
		self.status = False
	
	def run(self):
		if caseObj.identifyOSBit() == "64":
			cmd = "which mplayer"
			if getCmdResult(cmd) == "":
				return
		if caseObj.identifyOSBit() == "32":
			cmd = "which mplayer"
			if getCmdResult(cmd) == "":
				if os.path.isfile(g_resourcePath + "mplayer"):
					cmd = "echo " + passwd + " | sudo -S install -c -m 0755 " + g_resourcePath + "mplayer /usr/bin >/dev/null"
					os.system(cmd)
				else:
					return
			if not os.path.isfile("/usr/lib/i386-linux-gnu/libjpeg.so.62"):
				if os.path.isfile(g_resourcePath + "libjpeg.so.62"):
					cmd = "echo " + passwd + " | sudo -S install -c -m 0755 " + g_resourcePath + "libjpeg.so.62 /usr/lib/i386-linux-gnu >/dev/null"
					os.system(cmd)
				else:
					return

		self.status = True
		cmd = "mplayer -ontop " + self.videoname + " | tee " +  self.outputfile + " &"
		ret = os.system(cmd)
		time.sleep(5)
		keypress("<left>")
		keyrelease("<left>")
	
	def stop(self):
		cmd = "echo " + passwd + " | sudo -S killall mplayer 2>/dev/null"
		os.system(cmd)
		cmd = "echo " + passwd + " | sudo -S killall tee 2>/dev/null"
		os.system(cmd)

def getFrameLost(outputFile):
	cmd = "tail -n 1 " + outputFile + " | awk '{print $(NF - 2)}'"
	return getCmdResult(cmd)
	
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

def main():
	ISOTIMEFORMAT = "%Y-%m-%d %X"

	g_log.ilog(g_tag, "Concurrent processing capacity test begin.")
	print "Message from " + g_tag + ".py, Concurrent processing capacity begin.\n"

	doc = caseObj.getDocumentNode()
	data_node = caseObj.getXMLNode(doc, "data", 0)

	video_node = caseObj.getXMLNode(data_node, "video", 0)
	video = caseObj.getXMLNodeValue(video_node, 0)
	
	if os.path.basename(video) == video:		# 不是绝对路径
		video = g_resourcePath + video
		
	if not os.path.isfile(os.path.expanduser(video)):
		g_log.elog(g_tag, "Can not find video file. Test abort")
		print "Can not find video file. Test abort!"
		return

	outputFile_node = caseObj.getXMLNode(data_node, "output_file", 0)
	outputFile = caseObj.getXMLNodeValue(outputFile_node, 0)
	outputFile = g_resultPath + outputFile

	if os.listdir(g_resultPath):
		cmd = "echo " + passwd + " | sudo -S rm -rf " + g_resultPath + "* 2>/dev/null"
		os.system(cmd)

	sleepTime = 10

	fd = open(outputFile, "a")

	fd.write("测试时间: %s\n" % (time.strftime(ISOTIMEFORMAT, time.localtime())))

	curTime_1 = time.time()

	cmd = "sync"
	os.system(cmd)
	cmd = "echo " + passwd + " | sudo -S sh -c \"echo 3 > /proc/sys/vm/drop_caches\""
	os.system(cmd)

	videoObj = videoer(processFilename(video), outputFile + "~")
	videoObj.start()
	time.sleep(sleepTime + 5)
	if not videoObj.status:
		g_log.elog(g_tag, "mplayer doesn't exists. Can not play video.")
		print "mplayer doesn't exists, Can not play video. Test abort."
		videoObj.stop()
		fd.close()
		return

	lostFrame_1 = getFrameLost(outputFile + "~")
	fd.write("视频播放前" + str(sleepTime) + "秒总共丢帧数: %s\n" % (lostFrame_1))

	i = 0
	while True:
		if i == 8:
			break
		try:
			wps_file_node = caseObj.getXMLNode(data_node, "wps_file", i)
			i += 1
			wps_file = caseObj.getXMLNodeValue(wps_file_node, 0)
			wps_file_base = wps_file.split("/")[-1]
		except:
			g_log.wlog(g_tag, "wps_file node %d config error! Pls. check." % (i - 1))
			continue
		if os.path.basename(wps_file) == wps_file:
			wps_file = g_resourcePath + wps_file
		if not os.path.isfile(os.path.expanduser(wps_file)):
			g_log.wlog(g_tag, "File " + wps_file + " in wps_file config node %d not exist!" % (i - 1))
			continue
		time1 = time.time()
		lost1 = getFrameLost(outputFile + "~")
		openWPS(processFilename(wps_file))
		lost2 = getFrameLost(outputFile + "~")
		time2 = time.time()
		try:
			fd.write("打开文件%s过程中丢帧数: %d，平均每秒丢帧: %d\n" % (wps_file_base, int(lost2) - int(lost1), int(float(int(lost2)-int(lost1)) / (time2-time1))))
		except:
			pass
	
	lostFrame_2 = getFrameLost(outputFile + "~")
	curTime_2 = time.time()

	fd.write("视频播放" + str(int(curTime_2 - curTime_1)) + "秒后丢帧数: %s\n" % (lostFrame_2))
	fd.write("视频稳定后每秒平均丢帧数: %d\n\n" % ( int( float(int(lostFrame_2) - int(lostFrame_1)) / (curTime_2 - curTime_1 - float(sleepTime)) ) ))

	closeWPS()
	time.sleep(5)
	videoObj.stop()
	fd.write("下次测试结果会被覆盖，如果需要，请保存结果\n")
	fd.close()

	if os.path.isfile(outputFile + "~"):
		cmd = "rm -rf " + outputFile + "~"
		os.system(cmd)

	g_log.ilog(g_tag, "Concurrent processing capacity test done.")
	print "Message from " + g_tag + ".py, Concurrent processing capacity test done.\n"

if __name__ == "__main__":
	main()
