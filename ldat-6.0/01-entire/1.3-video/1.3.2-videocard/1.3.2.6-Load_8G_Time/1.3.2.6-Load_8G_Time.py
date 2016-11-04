#!/usr/bin/env python
#coding=utf-8

#脚本测试的前提:当前目录下必须有素材文件夹和素材文件
#素材文件夹:Load_Videos

import threading
import os
import sys
import commands
import xml.dom.minidom
import subprocess
#from ldtp      import *
#from ldtputils import *
from time      import sleep, time
from datetime  import datetime
#from gi.repository import Gtk, Wnck
import platform

#导入自己的线程类
from myThread import MyThread
reload(sys)   
sys.setdefaultencoding('utf8')  
#path control
g_publicLibPath = os.environ['AUTOTEST_PUBLIC_LIB']
sys.path.append(g_publicLibPath) 

#导入日志类
from logcase  import Logcase
from caseobject import CaseObject
#global log instance
mylog=Logcase() 
#*****************************************   
g_tag = '1.3.2.6-Load_8G_Time'
g_currentPath = sys.path[0]
#*****************************************
#全局参数
global NefName
global FName
global passwd  
global d1
global d2
global fName
global Uwname
global Gtk
global Wnck

d1=datetime.now()
d2=datetime.now()

#线程同步锁
mutex = threading.Lock()
#当前脚本对应 的绝对路径：
Path = os.path.abspath(os.path.dirname(sys.argv[0]))
Sshot = g_currentPath + '/resource/Sshot.sh '
Kcmd = "ps -ef | grep totem | grep -v grep | awk '{print $2}' | head -1 | xargs kill -9"
sysFile= g_currentPath+'/resource/sync.sh'
Tcmd = "ps -ef | grep mplayer | grep -v grep | awk '{print $2}' | head -1 | xargs kill -9"
Mcmd = "gnome-screenshot -f ./screenshot/`date +%H%M%S`"


#构建目录结构
def checkDir(dirName):
	try:
		if not os.path.exists(dirName):
			mylog.ilog(g_tag,'Beginning to create Pics Directory...' )
			if commands.getstatusoutput('mkdir ./resource')[0] == 0:
				os.system('mkdir ./result ./screenshot ')
				mylog.ilog(g_tag, 'Create ./resource successfully!')
			else:
				mylog.elog(g_tag, 'Create ./resource failed!')
				return False
		else:
			os.system('rm -rf ./result/* ./screenshot/*')
			mylog.ilog(g_tag,'./resouce has existed!' )
	except (NameError,Exception) as e:
		print e
	finally:
		return True

def getCmdResult(cmd):
	process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(o, e) = process.communicate()
	return o.strip()

def getCmdResult_new(cmd):
	process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	return process

#fName is the Filename to Load
def LoadTimes(fiName):
	if os.path.isfile("tmpfile"):
		cmd = "echo " + passwd + " | sudo -S rm -rf tmpfile 2>/dev/null"
		os.system(cmd)
	cmd = "mplayer %s | tee tmpfile &" % fiName
	beginTime = time()
	endTime = 0.0
	playTime = 0.0
	os.system(cmd)
	AudioCmd = "tail -n 1 tmpfile | awk 'BEGIN{OFS = \" \"} {print $(NF - 15), $(NF - 12)}'"
	while time() - beginTime < 60.0 :
		cmdResult = getCmdResult(AudioCmd)
		if cmdResult.split(" ")[0] == "A:" and float(cmdResult.split(" ")[1]) > 0.0:
			playTime = float(cmdResult.split(" ")[1])
			endTime = time()
			break

	cmd = "echo " + passwd + " | sudo -S killall mplayer 2>/dev/null"
	os.system(cmd)
	cmd = "echo " + passwd + " | sudo -S killall tee 2>/dev/null"
	os.system(cmd)
	if os.path.isfile("tmpfile"):
		cmd = "echo " + passwd + " | sudo -S rm -rf tmpfile 2>/dev/null"
		os.system(cmd)
	if endTime != 0.0:
		return (endTime - beginTime - playTime)
	else:
		return 0

def LoadTimes_smplayer(fiName):
	if os.path.isfile("tmpfile"):
		cmd = "echo " + passwd + " | sudo -S rm -rf tmpfile 2>/dev/null"
		os.system(cmd)
	cmd = "smplayer %s | tee tmpfile &" % fiName
	beginTime = time()
	endTime = 0.0
	playTime = 0.0
	playTime = time()
	os.system(cmd)
	AudioCmd = "tail -n 1 tmpfile | awk 'BEGIN{OFS = \" \"} {print $(NF - 15), $(NF - 12)}'"
	
	while time() - beginTime < 60.0 :
		cmdResult = getCmdResult_new(AudioCmd)
		sleep(4)
		if cmdResult is not None:
			endTime = time()
			break

	cmd = "echo " + passwd + " | sudo -S killall smplayer 2>/dev/null"
	os.system(cmd)
	cmd = "echo " + passwd + " | sudo -S killall tee 2>/dev/null"
	os.system(cmd)
	if os.path.isfile("tmpfile"):
		cmd = "echo " + passwd + " | sudo -S rm -rf tmpfile 2>/dev/null"
		os.system(cmd)
	if endTime != 0.0:
		return (endTime - beginTime - 4.0)
	else:
		return 0

#处理文件名中的空格
def proSpeace(oldName):
	newName = ""
	if len(oldName.split(" ")) > 1:
		for subpath in oldName.split(" "):
			newName += subpath + "\\" + " "
		newName = newName[:-2]
	else:
		newName = oldName
	return newName

#
def PosSpace(oldName):
	newName = ""
	tmpName = oldName.split('\\')
	if len(tmpName) > 1:
		for i in range(len(tmpName)):
			newName +=tmpName[i]
	else:
		newName = oldName
	return newName

#线程2 功能函数
def Screen(n):
	for i in range(5):
		os.system(Mcmd)
	#os.system(Sshot)
	os.system('killall totem')
	print 'curretn time is ',datetime.now()
	return 
				
#线程1 功能函数
def Splay(n):
	try:
		if mutex.acquire():
			os.system('totem %s & ' % FName)	
			while True:
				while Gtk.events_pending():
					Gtk.main_iteration()
					screen = Wnck.Screen.get_default()
					screen.force_update()
					wins = screen.get_windows()
				sleep(0.1)
				for w in wins:
					tName = w.get_name()
					if cmp(Uwname, tName) ==0:
						mutex.release()
						break 
	except Exception as e:
		print e
	finally:
		return 
				
				

#线程2 功能函数
def Stime(d1,d2):
	try:
		d1 = datetime.now()
		if mutex.acquire():
			mutex.release()
		d2 = datetime.now()
	except Exception as e:
		print e
	finally:
		return (d2 - d1)
				
	


#函数列表
funcs = [Splay, Stime]

def main():	
	global passwd
	global NefName	
	global d1,d2	
	global FName
	global fName
	global Uwname
	global Gtk
	global Wnck
	obj = CaseObject(g_tag, g_currentPath + '/' + g_tag + '.xml')
	#使用绝对路径创建日志文件
	Path = os.path.abspath(os.path.dirname(sys.argv[0]))
	os.chdir(Path)
	checkDir('./resource')
	os.system('touch ' + g_currentPath + '/result/result.log')
	doc = obj.getDocumentNode()
	#for count Node
	data_node0 = obj.getXMLNode(doc,'data',0)
	count_node = obj.getXMLNode(data_node0,'count',0)
	count =  obj.getXMLNodeValue(count_node, 0)
	print 'You will do times:' ,count
	#for file Name
	data_node1 = obj.getXMLNode(doc,'data',0)
	file_node = obj.getXMLNode(data_node1,'fName',0)
	fname =  obj.getXMLNodeValue(file_node, 0).strip()
	
	if not os.path.isfile(os.path.expanduser(fname)):
		print "Message from " + g_tag + ".py, video file %s not found.\n" % (fname)
		return
	#filer first and last space
	
	fName = os.path.basename(fname.strip())
	dirName = os.path.dirname(fname.strip())
	
	#进行转义
	NefName= proSpeace(fName)
	#totem 加载文件名称
	FName = '%s/%s' % (dirName, NefName)
	#名称准转换
	Uwname = fName.encode('utf-8')
	passwd = obj.getPasswd()
	os_type = obj.getOSName()

	if(os_type != "kylin-V4"):
		from gi.repository import Gtk, Wnck

	for i  in range(count):
		if os.path.exists(sysFile):
			os.system('chmod a+x %s' % sysFile)
			os.system('echo %s | sudo -S sh %s' % (passwd, sysFile))
		else:
			print 'sync memory shell script not exist  and exit!'
			sys.exit()
		#************************************************************
		#threads array
		#if (cmp(os_type,'cos') ==0) or (cmp(os_type, 'isoft') ==0):
		if platform.architecture()[0] == "32bit":
			threads = []
			nfuncs = range(len(funcs))
			#启动线程
			t1 = MyThread(Splay,'0',Splay.__name__)
			threads.append(t1)
			t2 = MyThread(Stime,(d1,d2),Stime.__name__)
			threads.append(t2)

			for i in nfuncs:
				threads[i].start()
	
			for i in nfuncs:	
				threads[i].join()
			os.system('killall totem')
			#计算时间
			d = t2.getResult()
			print 'Load time  is:' ,d
			times = str(d.seconds) + '.' + str(d.microseconds)
			period =float(times)
		elif cmp(os_type,'kylin') ==0:
			period = LoadTimes(proSpeace(fname))
			#os.system(Tcmd)
		elif (cmp(os_type,'cos') ==0) or (cmp(os_type, 'kylin-V4') ==0):
			period = LoadTimes_smplayer(proSpeace(fname))
		#两种操作系统都需要
		resultStr = "Load file: %s Use : %f S" % (NefName, period)
		cmd = "echo \"" + resultStr + "\" >>" + g_currentPath + "/result/result.log"
		os.system(cmd)
		sleep(5)
	sys.exit()

if __name__ == '__main__':
	main()
