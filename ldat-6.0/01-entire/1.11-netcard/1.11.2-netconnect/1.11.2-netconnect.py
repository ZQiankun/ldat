#coding=utf-8
__main__="__main__"

from ldtp import *
from ldtputils import *
import time
import os
import logging
import sys
import string
import getpass #modified by luzh

g_currentPath = sys.path[0]
sys.path.append(os.environ['AUTOTEST_PUBLIC_LIB'])

picdir = '/resource/'
outdir = '/result/'

if not os.path.exists(g_currentPath + picdir):
    os.system('mkdir -p '+ g_currentPath + picdir)

if not os.path.exists(g_currentPath + outdir):
    os.system('mkdir -p '+ g_currentPath + outdir)

from logcase import Logcase
from caseobject import CaseObject
g_log = Logcase()

picobj = CaseObject('1.11.2-netconnect',g_currentPath + '/1.11.2-netconnect.xml')
doc = picobj.getDocumentNode()
g_osName = picobj.getOSName()

from screenshot import Screenshot
g_sst = Screenshot()

common_node = picobj.getXMLNode(doc,'common',0)
count_node = picobj.getXMLNode(common_node, 'count', 0)
count = picobj.getXMLNodeValue(count_node, 0)

data_node = picobj.getXMLNode(doc,'data',0)
web_site_n = picobj.getXMLNode(data_node, 'web_site', 0)
web_site = picobj.getXMLNodeValue(web_site_n ,0)

show_time_n = picobj.getXMLNode(data_node, 'show_time', 0)
show_time = picobj.getXMLNodeValue(show_time_n ,0)

def ping_web_site():
    os.system('killall firefox')
    os.system('ping www.baidu.com -c 5 > '+g_currentPath + outdir+'ping.txt &')

    return

def video_on_line():
    os.system('firefox --new-window '+web_site+' &')
    time.sleep(show_time)
    g_sst.scrprint('1.11.2-netconnect', 'video_on_line', g_currentPath)

    return

def close_firefox():
    os.system('killall firefox')
    return 

def main():
	if g_osName == 'cos':
		ping_web_site()
		video_on_line()
		close_firefox()
        	return

	if g_osName == 'kylin':
		ping_web_site()
		video_on_line()
		close_firefox()
		return

	if g_osName == 'isoft':
		ping_web_site()
		video_on_line()
		close_firefox()
		return

if __main__=="__main__":
    main()
