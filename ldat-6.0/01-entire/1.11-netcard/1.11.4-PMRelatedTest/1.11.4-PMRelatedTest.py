#! /usr/bin/env python
#coding=utf-8
# 1.11.4 power management related test
# 1.11.4-pm_related_test.py

import os
import sys
import subprocess
import time
from ldtp import *

reload(sys)
sys.setdefaultencoding("utf8")

g_tag = "1.11.4-PMRelatedTest"
g_currentPath = sys.path[0]
g_publicLibPath = os.environ['AUTOTEST_PUBLIC_LIB']
sys.path.append(g_publicLibPath)

from logcase import Logcase
from caseobject import CaseObject
from screenshot import Screenshot

g_log = Logcase()
networkWithPmRelatedTestObj = CaseObject("networkWithPmRelatedTest", g_currentPath + "/" + g_tag + ".xml")

outputFile = "1.11.4-result"
video_show_time = 30
passwd = networkWithPmRelatedTestObj.getPasswd()
osname = networkWithPmRelatedTestObj.getOSName()

def getCmdResult(cmd):
	process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(o, e) = process.communicate()
	return o

def S3(time):
	g_log.ilog(g_tag, "System will fall into S3 immediately. After " + str(time) + " seconds will be woke up.")
	if osname == "isoft":
		cmd = "echo " + passwd + " | sudo -S rtcwake -u -m mem -s " + str(time)
	else:
		cmd = "echo " + passwd + " | sudo -S rtcwake -m mem -s " + str(time)
	os.system(cmd)
	
def S4(time):
	if os.environ["S4_ENABLE"] == "1":
		g_log.ilog(g_tag, "System will fall into S4 immediately. After " + str(time) + " seconds will be woke up.")
		if osname == "isoft":
			cmd = "echo " + passwd + " | sudo -S rtcwake -u -m disk -s " + str(time)
		else:
			cmd = "echo " + passwd + " | sudo -S rtcwake -m disk -s " + str(time)
		os.system(cmd)
	
def openOnlineVideo(url):
	cmd = "firefox --new-window " + url + " >/dev/null 2>&1 &"
	if not os.system(cmd):
		activatewindow("*Firefox*")
		return True
	activatewindow("*Firefox*")
	return False
	
def closeFirefox():
	for i in range(10):
		if guiexist("*Firefox*"):
			closewindow("*Firefox*")
			time.sleep(1)
			if guiexist("*dlg*"):
				if osname == "kylin":
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

def setgrub():
	if networkWithPmRelatedTestObj.getOSName() != "kylin":
		cmd = "echo " + passwd + " | sudo -S chmod a+w /boot/grub/grub.cfg >/dev/null"
		os.system(cmd)
		cmd = "echo " + passwd + " | sudo -S sed -i s/timeout=-1/timeout=1/g /boot/grub/grub.cfg >/dev/null"
		os.system(cmd)
		cmd = "echo " + passwd + " | sudo -S chmod a-w /boot/grub/grub.cfg >/dev/null"
		os.system(cmd)

def resetgrub():
	if networkWithPmRelatedTestObj.getOSName() != "kylin":
		cmd = "echo " + passwd + " | sudo -S chmod a+w /boot/grub/grub.cfg >/dev/null"
		os.system(cmd)
		cmd = "echo " + passwd + " | sudo -S sed -i s/timeout=1/timeout=-1/g /boot/grub/grub.cfg > /dev/null"
		os.system(cmd)
		cmd = "echo " + passwd + " | sudo chmod a-w /boot/grub/grub.cfg >/dev/null"
		os.system(cmd)

def main():
	doc = networkWithPmRelatedTestObj.getDocumentNode()
	data_node = networkWithPmRelatedTestObj.getXMLNode(doc, "data", 0)
	online_video_site_node = networkWithPmRelatedTestObj.getXMLNode(data_node, "online_video_site", 0)
	online_video_site = networkWithPmRelatedTestObj.getXMLNodeValue(online_video_site_node, 0)	#online_video_site
	sleep_time_node = networkWithPmRelatedTestObj.getXMLNode(data_node, "sleep_time", 0)
	sleep_time = networkWithPmRelatedTestObj.getXMLNodeValue(sleep_time_node, 0)			#sleep_time

	resultPath = g_currentPath + "/result/"
	screenshotPath = g_currentPath + "/screenshot/"

	if os.listdir(resultPath):
		cmd = "echo " + passwd + " | sudo -S rm -rf " + resultPath + "* 2>/dev/null"
		os.system(cmd)
	if os.listdir(screenshotPath):
		cmd = "echo " + passwd + " | sudo -S rm -rf " + screenshotPath + "* 2>/dev/null"
		os.system(cmd)

	screenshotName = ""
	if os.environ["S3_ENABLE"] == "1":
		screenshotName += "S3"
	if os.environ["S4_ENABLE"] == "1":
		screenshotName += "S4"

	g_log.ilog(g_tag, "`Network test power management related test begin.'")
	print "Message from " + g_tag + ".py, `Network test power management related test begin.'"

	setgrub()

	# 第一次睡眠
	if os.environ["S3_ENABLE"] == "1":
		print "Message from " + g_tag + ".py, System will fall into S3 immediately. After " + str(sleep_time) + " seconds will be woke up"
		time.sleep(1)
		S3(sleep_time)
		g_log.ilog(g_tag, "System wake up from S3.")
		print "Message from " + g_tag + ".py, System wake up from S3."

	time.sleep(5)

	if os.environ["S4_ENABLE"] == "1":
		print "Message from " + g_tag + ".py, System will fall into S4 immediately. After " + str(sleep_time) + " seconds will be woke up"
		time.sleep(1)
		S4(sleep_time)
		g_log.ilog(g_tag, "System wake up from S4.")
		print "Message from " + g_tag + ".py, System wake up from S4."
	
	if screenshotName != "":
		cmd = "echo \"%s操作唤醒后查看网络连接状态：\" >" + resultPath + outputFile
		os.system(cmd % (screenshotName))
	else:
		cmd = "echo \"查看网络链接状态：\" >" + resultPath + outputFile
		os.system(cmd)

	test_site = "www.baidu.com"
	cmd = "ping " + test_site + " -c 5 2>&1 | tee -a " + resultPath + outputFile
	os.system(cmd)

	fd = open(resultPath + outputFile, "a")
	fd.write("\n网页在线视频播放信息请到screenshot目录查看！\n\n")
	fd.write("下次测试结果将会被覆盖，如果有需要，请保存好结果。")
	fd.close()
	
	# 在线视频观看
	closeFirefox()
	if not openOnlineVideo(online_video_site):
		g_log.Wlog(g_tag, "Open online video failed.")
	time.sleep(video_show_time)
	shotObj = Screenshot()
	shotObj.scrprint(g_tag, "1_" + screenshotName + "_", g_currentPath)
	
	# 第二次睡眠
	if os.environ["S3_ENABLE"] == "1":
		print "Message from " + g_tag + ".py, System will fall into S3 immediately. After " + str(sleep_time) + " seconds will be woke up"
		time.sleep(1)
		S3(sleep_time)
		g_log.ilog(g_tag, "System wake up from S3.")
		print "Message from " + g_tag + ".py, System wake up from S3."
		time.sleep(10)
		shotObj.scrprint(g_tag, "2_S3_", g_currentPath)
		time.sleep(video_show_time)

	if os.environ["S4_ENABLE"] == "1":
		print "Message from " + g_tag + ".py, System will fall into S4 immediately. After " + str(sleep_time) + " seconds will be woke up"
		time.sleep(1)
		S4(sleep_time)
		g_log.ilog(g_tag, "System wake up from S4.")
		print "Message from " + g_tag + ".py, System wake up from S4."
	
	# 查看视频是否正常播放
	time.sleep(10)
	shotObj.scrprint(g_tag, "2_" + screenshotName + "_", g_currentPath)
	time.sleep(video_show_time)
	shotObj.scrprint(g_tag, "lasttime", g_currentPath)
	
	resetgrub()
	
	closeFirefox()

	g_log.ilog(g_tag, "`Network test power management related test done.'")
	print "Message from " + g_tag + ".py, `test done.'"
	
	return

if (__name__ == "__main__"):
	main()
