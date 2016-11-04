#coding=utf-8
__main__="__main__"

from ldtp import *
from ldtputils import *
import time
import os
import logging
import sys
import string
import getpass 
import codecs 
import subprocess

g_tag = "1.11.5-PowerAndNetwork"
g_currentPath = sys.path[0]
sys.path.append(os.environ['AUTOTEST_PUBLIC_LIB'])


picdir = '/result/'

if not os.path.exists(g_currentPath + picdir):
	os.system('mkdir -p '+ g_currentPath + picdir)

if os.path.exists(g_currentPath + picdir+'pingLog.txt'):
	os.system('rm -rf '+ g_currentPath + picdir+'pingLog.txt')

screendir='/screenshot/'
if not os.path.exists(g_currentPath + picdir):
	os.system('mkdir -p '+ g_currentPath + screendir)

if os.path.exists(g_currentPath + picdir):
	os.system('rm -rf '+ g_currentPath + screendir)


from logcase import Logcase
from caseobject import CaseObject
g_log = Logcase()

caseObj = CaseObject(g_tag, g_currentPath + "/" + g_tag + ".xml")
passwd = caseObj.getPasswd()

from screenshot import Screenshot
g_sst = Screenshot()

#parse xml
picobj = CaseObject('1.11.5-PowerAndNetwork',g_currentPath + '/1.11.5-PowerAndNetwork.xml')
doc = picobj.getDocumentNode()

common_node = picobj.getXMLNode(doc,'common',0)
count_node = picobj.getXMLNode(common_node, 'count', 0)
count = picobj.getXMLNodeValue(count_node, 0)


g_osName = picobj.getOSName()
print g_osName


def s3():
	g_log.ilog('1.11.5-PowerAndNetwork','Enter s3 rtcwake')
	cmd = "echo " + passwd + " | sudo -S rtcwake -m mem -s 120"
	os.system(cmd)

def s4():
	g_log.ilog('1.11.5-PowerAndNetwork','Enter s4 rtcwake')
	cmd = "echo " + passwd + " | sudo -S rtcwake -m disk -s 120"
	os.system(cmd)
	
def lookupNetstat():
	g_log.ilog('1.11.5-PowerAndNetwork','Enter  lookupNetstat')
	commandline = "ping www.baidu.com -c 3"
	p = subprocess.Popen(commandline,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
	(result,e) = p.communicate()
	return result

def Screensave(name):
	g_log.ilog('1.11.5-PowerAndNetwork','Enter  screensave')
	g_sst.scrprint('1.11.5-PowerAndNetwork',name,g_currentPath)

def openWebVideo():
	g_log.ilog('1.11.5-PowerAndNetwork','Enter  openWebVideo')
	cmd = '/usr/bin/firefox -new-window "http://www.iqiyi.com/v_19rrmaodaw.html?vfm=f_109_bdxs" &'
	os.system(cmd)
	time.sleep(20)	

def closeWebVideo():
	g_log.ilog('1.11.5-PowerAndNetwork','Enter  closeWebVideo')
	os.system("killall firefox")
	#keypress('<alt>')
	#keypress('f4')
	#keyrelease('<alt>')
	#keyrelease('f4')

def main():
	os.system(g_currentPath + '/resource/back-default-set-ip.sh ' + passwd)	
	time.sleep(3)
	f=codecs.open( g_currentPath + picdir+'pingLog.txt','w','utf-8')
	#先s3,s4再检查网络播放视频.
	f.write(u"进行s3,s4休眠操作,再检查网络播放视频" + '\n')
	for i in (3,4):	
		if i == 3:
			f.write(u"进行s3休眠操作" + '\n')
			s3()
			f.write(u"检查网络连接:" + '\n')
			result = lookupNetstat()
			f.write(result + '\n')
		
			openWebVideo()
			Screensave("VideoScreenAfterS3operation")
			closeWebVideo()
		else:
			f.write(u"进行s4休眠操作" + '\n')
			s4()
			f.write(u"检查网络连接:" + '\n')
			result = lookupNetstat()
			f.write(result + '\n')
		
			openWebVideo()
			Screensave("VideoScreenAfterS4operation")
			closeWebVideo()		
		
	#先播放视频再进入s3,s4.
	f.write(u"先播放视频,再执行s3,s4休眠操作,再播放视频" + '\n')
	
	for i in (3,4):
		openWebVideo()
		if i == 3:
			f.write(u"进行s3休眠操作" + '\n')
			s3()
			f.write(u"检查网络连接:" + '\n')
			result = lookupNetstat()
			f.write(result + '\n')
			Screensave("VideoBroadcastAndS3videoScreen")
			closeWebVideo()
		else:
			f.write(u"进行s4休眠操作" + '\n')
		   	s4()
			f.write(u"检查网络连接:" + '\n')
			result = lookupNetstat()
			f.write(result + '\n')
			Screensave("VideoBroadcastAndS4Videoscreen")		
			closeWebVideo()

	f.close()	
	os.system(g_currentPath + '/resource/set-static-ip.sh ' + passwd) 
	time.sleep(3)
	return 

if __main__=="__main__":
	main()
