#! /usr/bin/env python
#coding=utf-8


import os
import sys
import subprocess
import time
import threading

reload(sys)
sys.setdefaultencoding("utf8")

g_tag = "1.2.13-PowerAndLockInfo"
g_currentPath = sys.path[0]
g_publicLibPath = os.environ['AUTOTEST_PUBLIC_LIB']
sys.path.append(g_publicLibPath)

from logcase import Logcase
from caseobject import CaseObject
from screenshot import Screenshot
from ldtp import *

picdir = '/screenshot/'

if os.path.exists(g_currentPath + picdir):
        os.system('rm -rf '+ g_currentPath + picdir)

g_log = Logcase()

caseObj = CaseObject(g_tag, g_currentPath + "/" + g_tag + ".xml")

shotObj = Screenshot()

passwd = caseObj.getPasswd()

osname = caseObj.getOSName()


scriptFile = g_currentPath + "/resource/" + "usbKM.sh"

lockThread = None

forwardDelay = None
backDelay = None

from screenshot import Screenshot
g_sst = Screenshot()

def getCmdResult(cmd):
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (o, e) = process.communicate()
        return o.strip()

def Screensave(name):
        g_log.ilog(g_tag,'Enter  screensave')
        g_sst.scrprint(g_tag, name, g_currentPath)

def openPowerManagement():
	os.system("cinnamon-settings power&")
	time.sleep(5)

def closePowerManagement():
	#os.system("killall cinnamon-settings")
	g_log.ilog(g_tag,"Enter close PowerManagement")
	#keypress('<alt>')
	#keyrelease('<F4>')
	#time.sleep(5)
	#g_log.ilog(g_tag,"Exit close PowerManagement")
	num = getCmdResult("ps -ef |grep \"cinnamon-settings.py power\"|sed -n '1p'|awk '{print $2;}'")
	os.system("kill " + num)
	return 
	

def openScreenManagement():
	os.system("cinnamon-settings screensaver&")
	time.sleep(5)

def closeScreenManagement():
	#os.system("killall cinnamon-settings")
	#keypress('<alt>')
	#keyrelease('<f4>')
	#time.sleep(3)
	num = getCmdResult("ps -ef |grep \"cinnamon-settings.py screensaver\"|sed -n '1p'|awk '{print $2;}'")
	os.system("kill " + num)
	g_log.ilog(g_tag, "Enter closeScreenManagement")
	return 

def upArrow(n):
	for i in range(1, n+1) :
		keypress('<up>')
		keyrelease('<up>')
def downArrow(n):
	for i in range(1, n+1) :
		keypress('<down>')
		keyrelease('<down>')
def tabPress(n):
	g_log.ilog(g_tag, "Enter tabPress")
	for i in range(1,n+1) :
		g_log.ilog(g_tag, "Enter tabPress1")
		keypress('<tab>')
		keyrelease('<tab>')

#电源选项没有单选按钮,可以设置一个初始状态.
#调用电源管理接口后,各个选项状态如下:
# 	在此时间内无操作则关闭屏幕:从不
#	在此时间内无操作则挂起	  :从不
#	当电源按钮按下时	  :无操作 (注:在系统默认状态中,该选项默认是询问)
#	在此时间内无操作则启动屏幕保护:  从不
def resetPowerManagement():
	openPowerManagement()	
	tabPress(1)
	for i in range(1,5):
		tabPress(1)
		for i in range(1,7):
			downArrow(i)	

	closePowerManagement()
	return 
#给每一个选项编号,需要那个选项输入编号即可.
#按默认的来,而且
#事先调用得按照顺序来.
def selectPowerManagement(num):
	openPowerManagement()
	tabPress(1)
	#在此时间内无操作则关闭屏幕
	#[从不=0 ,1小时 = 1, 30分钟 = 2, 10分钟 = 3, 5分钟 = 4]
	if num == 0 or num == 1 or num == 2 or num == 3 or num == 4:
		tabPress(1)
		upArrow(num)
		
	#在此时间内无操作则挂起
	#[从不=5, 5分钟=9, 10分钟=8, 30分钟=7, 1小时=6]
	elif num == 5 or num == 6 or num == 7 or num == 8 or num == 9 :
		tabPress(2)
		upArrow(num-5)
	#当电源按钮按下时
	#[无操作=10, 锁屏=14, 挂起=14, 立即关闭=13, 休眠=12, 询问=11]
	elif num == 10 or num == 11 or num == 12 or num == 13 or num == 14 or num == 15:
		tabPress(3)
		upArrow(num-10)

	#在此时间内无操作则启动屏幕保护.
	#[ 3分钟=20, 8分钟=19, 15分钟=18, 45分钟=17, 从不=16]
	elif num == 16 or num == 17 or num == 18 or num == 19 or num == 20 :
		tabPress(4)
		downArrow(num-16)
	
	closePowerManagement()
	return 

#类似selectScreenManagement,给每一个选项编号.
def selectScreenManagement(selected):
	g_log.ilog(g_tag, "Enter selectPowerManagement")
	openScreenManagement()
	tabPress(1)
	#[锁定设置]
	# 睡眠时关闭电脑= 0
	if selected == 0:
		tabPress(1)
		keypress('<enter>') 
		keyrelease('<enter>')

	elif selected == 1:
		tabPress(selected+1)
		keypress('<enter>')
		keyrelease('<enter>')
	# 屏幕关闭时锁定电脑 = 1
	# 选中屏幕关闭时锁定电脑 立即= 2, 15秒之后=3,30秒之后=4,1分钟之后=5,2分钟之后=6,3分钟之后=7,
	#			 5分钟之后=8,10分钟之后=9,30分钟之后=10,1小时之后=11 
	elif selected <= 11 and selected >= 2 :
		tabPress(3)	
		downArrow(1)
	#屏幕锁定时显示离开消息 = 12

	#当从菜单锁定屏幕时询问自定信息 = 13
	elif selected == 13 :
		g_log.ilog(g_tag, "Enter selected==13")
		tabPress(4)
		keypress('<enter>')
 		keyrelease('<enter>')
	else:
		return	

	closeScreenManagement()
	return 

#def keypressPasswd():
#	for i in range(len(passwd)):
#		keypress('passwd[i]')
#		keyrelease('passwd[i]')
#	keypress('<enter>')
#	keyrelease('<enter>')

def main():
	#case 154.1
	#电源选项中设置在此时间内无操作30分钟
	selectPowerManagement(4)
	#锁定屏幕,输入提示信息并确认
	os.system("cinnamon-screensaver-command --lock --away-message \"God is a girl\"")
	time.sleep(3)
	Screensave("EnsureQuoteMessage")
	time.sleep(1)
	os.system("cinnamon-screensaver-command -d")
	
	#case 154.2 检查屏幕关闭后,在指定时间内是否锁定屏幕.
	time.sleep(1)
	selectScreenManagement(1)
	for i in range(2,12) :
		selectScreenManagement(i)		
		timeval = 0
		if i == 2:
			timeval = 0
		elif i == 3:
			timeval = 15
		elif i == 4:
			timeval = 30
		elif i == 5:
			timeval = 60
		elif i == 6:
			timeval = 120
		elif i == 7:
			timeval = 180
		elif i == 8:
			timeval = 300
		elif i == 9:
			timeval = 600
		elif i == 10:
			timeval = 1800
		elif i == 11:
			timeval = 3600

		time.sleep(timeval + 300 )
		tt = '%ds' %timeval
		Screensave("closeScreenAndLockDelaytime" + tt)		
		keypress('<enter>')
		keyrelease('<enter>')
		#os.system("xset dpms force on")
		time.sleep(5)

	#case 154.3
	#设定锁定
	selectScreenManagement(1)
	os.system("xset dpms force off")
	g_log.ilog(g_tag,"Enter close screeen and lock screen right now")
	Screensave("closeScreenLockThencloseScreenLock154.3")
	time.sleep(1)
	os.system("xset dpms force on")
	#case 155.2
	
	#case 157,2,3 目前这个case仅仅是选中选项,然后sleep即可.
	#case 157.2 在此时间内无操作则关闭屏幕,分别设置5分钟,10分钟,30分钟,一小时,从不.
	for i in range(0,5):
		resetPowerManagement()
		selectPowerManagement(i)
		Screensave("closeScreenAndLock157.2" + '%d' %i)
		if i == 0:
		   g_log.ilog(g_tag,"Enter close screeen and lock screen right now")
		   continue
		elif i == 1:
		   time.sleep(3600)
		   g_log.ilog(g_tag,"Enter close screen and lock screen after one hour")
		elif i == 2:
		   time.sleep(1800)
		   g_log.ilog(g_tag,"Enter close screen and lock screen after half an hour")
		elif i == 3:
		   time.sleep(600)
		   g_log.ilog(g_tag,"Enter close screen and lock screen after 10 minites.")
		elif i == 4:
		   time.sleep(300)
		   g_log.ilog(g_tag,"Enter close screen and lock screen after 5 minutes.")
	#case 157.3 在此时间内无操作则挂起,分别设置5分钟,10分钟,30分钟,一小时,从不.
	for i in range(5,10):
		resetPowerManagement()
		selectPowerManagement(i)
		Screensave("closeScreenAndLock157.3" + '%d' %i)
		if i  == 5:
		   	g_log.ilog(g_tag,"Enter suspend close screeen and lock screen right now")
			continue
		elif i == 6:
		   	g_log.ilog(g_tag,"Enter suspend close screen  and lock screen after one hour")
			time.sleep(3600)
		elif i == 7:
		   	g_log.ilog(g_tag,"Enter suspend close screen and lock screen after half an hour")
			time.sleep(1800)
		elif i == 8:
		   	g_log.ilog(g_tag,"Enter suspend close screen and lock screen after 10 minites.")
			time.sleep(600)
		elif i == 9:
		   	g_log.ilog(g_tag,"Enter suspend close screen and lock screen after 5 minutes.")
			time.sleep(300)
	return 

if (__name__ == "__main__"):
	main()

	


