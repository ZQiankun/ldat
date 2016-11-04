#! /usr/bin/env python
#coding=utf-8
# 1.2.4 Screensaver and lock info
# 1.2.4-ScreensaverAndLockInfo.py

import os
import sys
import subprocess
import time
import threading

reload(sys)
sys.setdefaultencoding("utf8")

g_tag = "1.2.4-ScreensaverAndLockInfo"
g_currentPath = sys.path[0]
g_publicLibPath = os.environ['AUTOTEST_PUBLIC_LIB']
sys.path.append(g_publicLibPath)

from logcase import Logcase
from caseobject import CaseObject
from screenshot import Screenshot
from ldtp import *

g_log = Logcase()

caseObj = CaseObject(g_tag, g_currentPath + "/" + g_tag + ".xml")

shotObj = Screenshot()

passwd = caseObj.getPasswd()

osname = caseObj.getOSName()

cosConfigFile = "~/.xscreensaver"

scriptFile = g_currentPath + "/resource/" + "usbKM.sh"

lockThread = None

forwardDelay = None
backDelay = None

global WATCHTIMEFORMAT

def getCmdResult(cmd):
	process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(o, e) = process.communicate()
	return o.strip()

def chConfFile(filename, node, value):
	cmd = "sed -i \'s/%s:\s*\w*.*/%s:\t%s/g\' %s" % (node, node, value, filename)
	#print "cmd =", cmd		###################
	if os.system(cmd):
		return False
	return True

def runScreensaver():
	if osname == "cos":
		cmd = "xscreensaver &"
		os.system(cmd)
		resourcePath = g_currentPath + "/resource"
		if not os.path.isfile(resourcePath + "/.xscreensaver"):
			g_log.elog(g_tag, "Can not find .xscreensaver!")
			print "Can not find .xscreensaver!"
			return False
		cmd = "cp " + resourcePath + "/.xscreensaver " + cosConfigFile
		os.system(cmd)
		chConfFile(cosConfigFile, "mode", "one")
		chConfFile(cosConfigFile, "timeout", "1:00:00")
		time.sleep(10)
		cmd = "xscreensaver-command -restart"
		os.system(cmd)
		time.sleep(10)
		return True
	elif osname == "kylin":
		#TODO
		cmd = "ps -ef | grep mate-screensaver | grep -v grep"
		if getCmdResult(cmd) == "":
			cmd = "mate-screensaver &"
			os.system(cmd)

		cmd = "dconf write /org/mate/screensaver/idle-activation-enabled true"
		os.system(cmd)
		cmd = "dconf write /org/mate/screensaver/lock-enabled false"
		os.system(cmd)
		cmd = "dconf write /org/mate/desktop/session/idle-delay 60"
		os.system(cmd)
		
		time.sleep(5)
		cmd = "dconf update"
		os.system(cmd)
		time.sleep(5)
		return True
	elif osname == "isoft":
		return False
	else:
		return False

def stopScreensaver():
	if osname == "cos":
		chConfFile(cosConfigFile, "mode", "off")
		chConfFile(cosConfigFile, "lock", "False")
		return True
	elif osname == "kylin":
		cmd = "dconf write /org/mate/screensaver/idle-activation-enabled false"
		os.system(cmd)
		cmd = "dconf write /org/mate/desktop/session/idle-delay 10"
		os.system(cmd)
		time.sleep(5)
		cmd = "dconf update"
		os.system(cmd)
		time.sleep(5)
		return True
	else:
		return False
		
def chTimeout(timeout):
	if osname == "cos":
		ret = chConfFile(cosConfigFile, "timeout", timeout)
		time.sleep(10)
		return ret
	elif osname == "kylin":
		cmd = "dconf write /org/mate/desktop/session/idle-delay " + timeout
		os.system(cmd)
		time.sleep(5)
		cmd = "dconf update"
		os.system(cmd)
		time.sleep(5)
		return True
	else:
		return False

def setLock():
	if osname == "cos" or osname == "isoft":
		if osname == "cos":
			chConfFile(cosConfigFile, "mode", "off")
			chConfFile(cosConfigFile, "lock", "False")
		cmd = "gsettings set org.gnome.desktop.screensaver lock-enabled true"
		os.system(cmd)
		time.sleep(5)
		return True
	elif osname == "kylin":
		cmd = "dconf write /org/mate/screensaver/idle-activation-enabled true"
		os.system(cmd)
		cmd = "dconf write /org/mate/screensaver/lock-delay 0"
		os.system(cmd)
		cmd = "dconf write /org/mate/screensaver/lock-enabled true"
		os.system(cmd)
		time.sleep(5)
		cmd = "dconf update"
		time.sleep(5)
		return True
	else:
		return False

def stopLock():
	if osname == "cos" or osname == "isoft":
		cmd = "gsettings set org.gnome.desktop.screensaver lock-enabled false"
		os.system(cmd)
		time.sleep(5)
		return True
	elif osname == "kylin":
		cmd = "dconf write /org/mate/screensaver/lock-enabled false"
		os.system(cmd)
		time.sleep(5)
		return True
	else:
		return False

def chLockDelay(delay):
	if osname == "cos" or osname == "isoft":
		cmd = "gsettings set org.gnome.desktop.screensaver lock-delay " + delay
		os.system(cmd)
		time.sleep(10)
		return True
	elif osname == "kylin":
		cmd = "dconf write /org/mate/desktop/session/idle-delay " + delay
		os.system(cmd)
		time.sleep(5)
		cmd = "dconf update"
		os.system(cmd)
		time.sleep(5)
		return True
	else:
		return False

def blankScreen():
	if osname == "cos" or osname == "isoft":
		cmd = "xset dpms force off && gnome-screensaver-command -a"
		os.system(cmd)
		time.sleep(15)

def unblankScreen():
	if osname == "cos" or osname == "isoft":
		keypress("<enter>")
		keyrelease("<enter>")
		#cmd = "xset dpms force on"
		#os.system(cmd)
	
def resetIdle():
	if osname == "cos":
		cmd = "xscreensaver-command -deactivate > /dev/null 2>&1"
		os.system(cmd)
		return True
	elif osname == "isoft":
		return True
	elif osname == "kylin":
		cmd = "mate-screensaver-command -p"
		os.system(cmd)
		return True
	else:
		return False

def inputPasswd():
	for key in passwd:
		keypress("<" + key + ">")
		keyrelease("<" + key + ">")
	keypress("<enter>")
	keyrelease("<enter>")
		
def formatTime(configTime, test):
	if osname == "cos" or osname == "isoft":
		if test == "screensaver":
			if configTime[-1] == "H" or configTime[-1] == "h":
				formattime = "%s:00:00" % (configTime[:-1]) if (int(configTime[:-1]) <= 12) else ("")
			elif configTime[-1] == "M" or configTime[-1] == "m":
				hours = int(configTime[:-1]) / 60
				minutes = int(configTime[:-1]) % 60
				formattime = "%1d:%02d:00" % (hours, minutes) if ((hours >= 1 and hours <= 12) or (hours == 0 and minutes >= 1)) else ("")
			elif configTime[-1] == "S" or configTime[-1] == "s":
				hours = int(configTime[:-1]) / 3600
				minutes = (int(configTime[:-1]) % 3600) / 60
				formattime = "%1d:%02d:00" % (hours, minutes) if ((hours >= 1 and hours <= 12) or (hours == 0 and minutes >= 1)) else ("")
			else:
				 formattime = ""
		if test == "lock":
			if configTime[-1] == "H" or configTime[-1] == "h":
				formattime = str ( "" if (int(configTime[:-1]) > 1) else (int(configTime[:-1] * 3600)) )
			elif configTime[-1] == "M" or configTime[-1] == "m":
				formattime = str ( "" if (int(configTime[:-1]) > 60 ) else (int(configTime[:-1]) * 60) )
			elif configTime[-1] == "S" or configTime[-1] == "s":
				formattime = str ( "" if (int(configTime[:-1]) > 3600) else (int(configTime[:-1])) )
			else:
				 formattime = ""
	elif osname == "kylin":
		if configTime[-1] == "H" or configTime[-1] == "h":
			formattime = str ( "" if (int(configTime[:-1]) * 60 > 120) else (int(configTime[:-1]) * 60) )
		elif configTime[-1] == "M" or configTime[-1] == "m":
			formattime = str ( "" if (int(configTime[:-1]) > 120) else (int(configTime[:-1])) )
		elif configTime[-1] == "S" or configTime[-1] == "s":
			formattime = str ( "" if (int(configTime[:-1]) / 60 > 120 or int(configTime[:-1]) / 60 < 1 ) else (int(configTime[:-1]) / 60) )
		else:
			formattime = ""
	else:
	  	formattime = ""
	return formattime

def disableXinput():
	cmd = "echo " + passwd + " | sudo -S " + scriptFile + " disable"
	os.system(cmd)

def enableXinput():
	cmd = "echo " + passwd + " | sudo -S " + scriptFile + " enable"
	os.system(cmd)

def setDelay():
	global forwardDelay
	global backDelay
	forwardDelay = 2
	if osname == "cos" or osname == "isoft":
		backDelay = 5
	elif osname == "kylin":
		backDelay = 15
	else:
		return False

def watch(ofile):
	if osname == "cos":
		cmd = "xscreensaver-command -watch >" + ofile + " &"
		os.system(cmd)

def killwatch():
	if osname == "cos":
		cmd = "ps -ef | grep \"xscreensaver-command -watch\" | grep -v grep | awk '{print $2}' | xargs kill -9"
		os.system(cmd)

def getExpectTime(configTime):
	if configTime[-1] == 'H' or configTime == 'h':
		return time.strftime(WATCHTIMEFORMAT, time.localtime(time.time() + int(configTime[:-1]) * 60 * 60))
	elif configTime[-1] == 'M' or configTime == 'm':
		return time.strftime(WATCHTIMEFORMAT, time.localtime(time.time() + int(configTime[:-1]) * 60))
	else:
		return time.strftime(WATCHTIMEFORMAT, time.localtime(time.time() + int(configTime[:-1])))

def main():
	global WATCHTIMEFORMAT
	ISOTIMEFORMAT = "%Y-%m-%d %X"
	WATCHTIMEFORMAT = "%a %b %d %X %G"
	
	screenshotPath = g_currentPath + "/screenshot"
	
	if os.path.exists(screenshotPath):
		cmd = "echo " + passwd + " | sudo -S rm -rf " + screenshotPath + "/* >/dev/null 2>&1"
		os.system(cmd)

	print "Message from " + g_tag + ".py, Screensaver and lock info test begin."
	g_log.ilog(g_tag, "Screensaver and lock info test begin.")

	if not os.path.isfile(scriptFile):
		g_log.elog(g_tag, "Script file for disable USB keyboard and mouse not exist.")
		print "Script file for disable USB keyboard and mouse not exist."
		return
	else:
		cmd = "echo " + passwd  + " | sudo -S chmod a+x " + scriptFile + " >/dev/null"
		os.system(cmd)
	
	if not runScreensaver():
		if osname != "isoft":
			print "Message from " + g_tag + ".py, Error on function runScreensaver()."
			g_log.elog(g_tag, "Error on function runScreenSaver().")
			return
		else:
			print "警告：普华系统没有提供屏保功能，跳过屏保功能测试，如有配置锁屏测试，锁屏测试正常进行"
			g_log.wlog(g_tag, "isoft OS don't provide screensaver function. skip screensaver test.")
	
	doc = caseObj.getDocumentNode()
	data_node = caseObj.getXMLNode(doc, "data", 0)
	output_file_node = caseObj.getXMLNode(data_node, "output_file", 0)
	outputFile = caseObj.getXMLNodeValue(output_file_node, 0)
	outputFile = g_currentPath + "/result/" + outputFile

	fd = open(outputFile, "a")
	
	setDelay()

	watch(outputFile + "~")
	
	print "\nMessage from " + g_tag + ".py, Mouse and Keyboard disabled!!!\n"
	disableXinput()

	# #############################
	timeout_node = caseObj.getXMLNode(data_node, "timeout", 0)
	try:
		timeoutlist = caseObj.getXMLNodeValue(timeout_node, 0)
	except:
		timeoutlist = None
	if osname == "isoft":
		timeoutlist = None
	if timeoutlist != None and timeoutlist != "":
		print "屏保测试开始\n"
		for configTime in timeoutlist.split(","):
			configTime = configTime.strip()
			timeout = formatTime(configTime, "screensaver")
			if timeout == "":
				continue
			chTimeout(timeout)

			resetIdle()

			fd.write("屏保测试 %s\n" % (configTime))
			fd.write("开始时间:         %s\n" % (time.strftime(WATCHTIMEFORMAT, time.localtime())))
			fd.write("正常进入屏保时间: %s\n" % (getExpectTime(configTime)))
			
			g_log.ilog(g_tag, "Testting screensaver timeout set %s. Idle time begin: %s." % (configTime, time.strftime(ISOTIMEFORMAT, time.localtime())))
			print "Testting screensaver timeout set %s. Idle time begin: %s." % (configTime, time.strftime(ISOTIMEFORMAT, time.localtime()))

			if configTime[-1] == "H" or configTime[-1] == "h":
				sleepTime = int(configTime[:-1]) * 3600
			elif configTime[-1] == "M" or configTime[-1] == "m":
				sleepTime = int(configTime[:-1]) * 60
			else:
				sleepTime = int(configTime[:-1])
			time.sleep(sleepTime - forwardDelay)

			shotObj.scrprint(g_tag, "屏保_" + configTime + "_前" + str(forwardDelay) + "S_", g_currentPath)

			time.sleep(forwardDelay + backDelay)	# 额外睡眠时间，中标屏保进入比较慢

			if osname == "cos":
				cmd = "sed '/RUN\s\d*/d' " + outputFile + "~ | tail -n 1"
				blankInfo = getCmdResult(cmd)
				#print blankInfo	######
				if blankInfo.split(" ")[0] == "BLANK":
					fd.write("实际进入屏保时间: %s\n" % (blankInfo.split("BLANK")[1].strip()))
				else:
					fd.write("实际未进入屏保\n")
			elif osname == "kylin":
				cmd = "mate-screensaver-command -t"
				blankInfo = getCmdResult(cmd)
				#print blankInfo	######
				if len(blankInfo.split(" ")) == 3:
					fd.write("实际进入屏保时间: %s\n" % (time.strftime(WATCHTIMEFORMAT, time.localtime(time.time() - int(blankInfo.split(" ")[1])))))
				else:
					fd.write("实际未进入屏保\n")

			shotObj.scrprint(g_tag, "屏保_" + configTime + "_后" + str(backDelay) + "S_", g_currentPath)

			fd.write("截图文件: %s ， %s\n\n" % ("屏保_" + configTime + "_前" + str(forwardDelay) + "S_*.png", "屏保_" + configTime + "_后" + str(backDelay) + "S_*.png"))

			resetIdle()
			g_log.ilog(g_tag,"Screensaver timeout set %s, test done. End time: %s.\n" % (configTime, time.strftime(ISOTIMEFORMAT, time.localtime())))
			print "Screensaver timeout set %s, test done. End time: %s.\n" % (configTime, time.strftime(ISOTIMEFORMAT, time.localtime()))
		print "屏保测试结束\n"

	# #############################
	lockTimeout_node = caseObj.getXMLNode(data_node, "lockTimeout", 0)
	try:
		lockTimeoutlist = caseObj.getXMLNodeValue(lockTimeout_node, 0)
	except:
		lockTimeoutlist = None
	if lockTimeoutlist != None and lockTimeoutlist != "":

		setLock()

		print "锁屏测试开始\n"
		for configTime in lockTimeoutlist.split(","):
			configTime = configTime.strip()
			delay = formatTime(configTime, "lock")
			if delay == "":
				continue
			
			chLockDelay(delay)
		
			if osname == "kylin":

				resetIdle()

				fd.write("锁屏测试(屏保后锁屏) %s\n" % (configTime))
				fd.write("开始时间:         %s\n" % (time.strftime(WATCHTIMEFORMAT, time.localtime())))
				fd.write("正常屏幕锁定时间: %s\n" % (getExpectTime(configTime)))

				g_log.ilog(g_tag, "Testting screensaver_lock timeout set %s. Idle time begin: %s." % (configTime, time.strftime(ISOTIMEFORMAT, time.localtime())))
				print "Testting screensaver_lock timeout set %s. Idel time begin: %s." % (configTime, time.strftime(ISOTIMEFORMAT, time.localtime()))

				if configTime[-1] == "H" or configTime[-1] == "h":
					sleepTime = int(configTime[:-1]) * 3600
				elif configTime[-1] == "M" or configTime[-1] == "m":
					sleepTime = int(configTime[:-1]) * 60
				else:
					sleepTime = int(configTime[:-1])
				time.sleep(sleepTime - forwardDelay)

				shotObj.scrprint(g_tag, "锁屏_" + configTime + "_前" + str(forwardDelay) + "S_", g_currentPath)

				time.sleep(forwardDelay + backDelay)	# 额外睡眠时间，中标屏保进入比较慢

				cmd = "mate-screensaver-command -t"
				lockInfo = getCmdResult(cmd)
				#print lockInfo	######
				if len(lockInfo.split(" ")) == 3:
					fd.write("实际屏幕锁定时间: %s\n" % (time.strftime(WATCHTIMEFORMAT, time.localtime(time.time() - int(lockInfo.split(" ")[1])))))
				else:
					fd.write("实际未锁定屏幕\n")

				resetIdle()

				time.sleep(2)

				shotObj.scrprint(g_tag, "锁屏_" + configTime + "_后" + str(backDelay) + "S_", g_currentPath)

				fd.write("截图文件: %s ， %s\n\n" % ("锁屏_" + configTime + "_前" + str(forwardDelay) + "S_*.png", "锁屏_" + configTime + "_后" + str(backDelay) + "S_*.png"))

				g_log.ilog(g_tag, "Screensaver_lock timeout set %s, test done. End time: %s.\n" % (configTime, time.strftime(ISOTIMEFORMAT, time.localtime())))
				print "Screensaver_lock timeout set %s, test done. End time: %s.\n" % (configTime, time.strftime(ISOTIMEFORMAT, time.localtime()))

			elif osname == "cos" or osname == "isoft":

				blankScreen()
				
				fd.write( "锁屏测试(屏幕关闭%s后锁定屏幕) \n" % (configTime) )
				fd.write( "屏幕关闭时间:     %s\n" % (time.strftime(WATCHTIMEFORMAT, time.localtime())) )
				fd.write( "正常屏幕锁定时间: %s\n" % (getExpectTime(configTime)) )

				g_log.ilog(g_tag, "Testting screen lock lock_delay set %s. Screen blank time: %s" % (configTime, time.strftime(ISOTIMEFORMAT, time.localtime())))
				print "Testting screen lock lock_delay set %s. Screen blank time: %s" % (configTime, time.strftime(ISOTIMEFORMAT, time.localtime()))

				if configTime[-1] == "H" or configTime[-1] == "h":
					sleepTime = int(configTime[:-1]) * 3600
				elif configTime[-1] == "M" or configTime[-1] == "m":
					sleepTime = int(configTime[:-1]) * 60
				else:
					sleepTime = int(configTime[:-1])
				time.sleep(sleepTime + backDelay)

				#resetIdle()
				unblankScreen()
				time.sleep(10)		# 等待屏幕从黑屏状态 恢复

				cmd = "ps -ef | grep cinnamon-screensaver-dialog | grep -v grep | awk '{print $5}'"
				lockInfo = getCmdResult(cmd)
				if lockInfo == "" or lockInfo == None:
					fd.write("实际屏幕未锁定\n")
				else:
					fd.write("实际屏幕锁定时间: %s\n" % lockInfo)

				shotObj.scrprint(g_tag, "锁屏_" + configTime + "_", g_currentPath)

				fd.write("截图文件: %s\n\n" % ("锁屏_" + configTime + "_*.png"))

				g_log.ilog(g_tag, "Screen lock lock_delay set %s, test done. End time: %s.\n" % (configTime, time.strftime(ISOTIMEFORMAT, time.localtime())))
				print "Screen lock lock_delay set %s, test done. End time: %s.\n" % (configTime, time.strftime(ISOTIMEFORMAT, time.localtime()))

			inputPasswd()
			time.sleep(5)
			
		print "锁屏测试结束\n"

	# #############################
	enableXinput()
	print "Message from " + g_tag + ".py, Mouse and Keyboard enabled!!!\n"

	if os.path.isfile(outputFile + "~"):
		cmd = "rm -rf " + outputFile + "~"
		os.system(cmd)

	fd.close()

	killwatch()

	stopLock()

	stopScreensaver()

	g_log.ilog(g_tag, "Screensaver and lock info test done.")
	print "Message from " + g_tag + ".py, Screensaver and lock info test done."

	return

if (__name__ == "__main__"):
	main()

