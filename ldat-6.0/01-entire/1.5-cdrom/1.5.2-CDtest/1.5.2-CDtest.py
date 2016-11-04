#!/usr/bin/env python
#coding=utf-8

###########################################################################
#01-entire.py
#Module for entire machine test
###########################################################################
__main__ = '__main__'

from ldtp import *
from ldtputils import *
import time
import os
import sys
import logging
import string
import getpass
import subprocess


g_tag = '1.5.2-CDtest'
g_currentPath = sys.path[0]
g_publicLibPath = os.environ['AUTOTEST_PUBLIC_LIB']

sys.path.append(g_publicLibPath)

g_s4 = int(os.environ['S4_ENABLE'])
print "s4 enable is"
print g_s4

g_s3 = int(os.environ['S3_ENABLE'])
print "s3 enable is"
print g_s3

sourcedir = '/resource/'
media_dir = sourcedir + 'media'
music_tool = 'rhythmbox'
video_tool = 'smplayer'

from logcase import Logcase
from caseobject import CaseObject
g_log = Logcase()

sourceobj = CaseObject(g_tag,g_currentPath + '/1.5.2-CDtest.xml')
doc = sourceobj.getDocumentNode()
g_osName = sourceobj.getOSName()

from ldtppub import LDTPPub
g_ldtpObj = LDTPPub()
from screenshot import Screenshot
g_sst = Screenshot()


common_node = sourceobj.getXMLNode(doc,'common',0)
count_node = sourceobj.getXMLNode(common_node,'count',0)
count = sourceobj.getXMLNodeValue(count_node,0)

data_node = sourceobj.getXMLNode(doc,'data',0)

music_source_name = []
video_source_name = []

passwd = sourceobj.getPasswd()
print (passwd)

def umountSourceFile(src_dir):
	os.system('sudo ' + 'umount ' + g_currentPath+src_dir)
	print('umount source files successfully!!!')

def addsourcefile(src_dir):
    if not os.path.exists(g_currentPath+src_dir): 
	os.system('mkdir -p ' + g_currentPath + src_dir)
    cdpath = "mount | grep iso9660 | awk '{print $1}'"
    process = subprocess.Popen(cdpath,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    (o,e)=process.communicate()
    devName = o.strip()
    if devName == None:
	print('No device found')
	umountSourceFile(src_dir)
	g_log.wlog('please insert the CD/DVD first!!!')
	return
    os.system('sudo '+'mount '+ devName + ' ' + g_currentPath+src_dir)
    time.sleep(1)

    return (True)

def scanFiles_cos64(src_dir):
    print('---------scanFiles_cos60-----------')
    g_log.ilog(g_tag,'scanFiles_cos64')
    n = 0
    for (dirPath,subdir,subfiles) in os.walk(src_dir):
        for (files) in (subfiles):
            g_log.ilog(g_tag,files)
            music_source_name.append(files)
            print ('**********[ %s ]************')%(files)
            n = 1
            if len(music_source_name) == None:
       	        print('no music found')
                g_log.wlog('no music found')
                return
    return

def OpenMedia_cos64(src_dir,tools):
	print ('opening source')
	g_log.ilog(g_tag,'opening')
	os.system(tools+' ' + g_currentPath +src_dir+' &')
	time.sleep(7)
	return (True)

def PauseAndPlay_cos64():
        sourceobj.enableMouseKeyboard(False)
	print ('Is editing music')
	g_log.ilog(g_tag,'Is editing music')

	print('Pause2playMusic')
        keypress('<ctrl>')
	keypress(' ')
	time.sleep(2)
	keyrelease('<ctrl>')
	keyrelease(' ')
	time.sleep(2)
	g_sst.scrprint(g_tag,'PauseMusic',g_currentPath)
        sourceobj.enableMouseKeyboard(True)
	return (True)
def LastestBtn_cos64():
	print('LastMusic')
        sourceobj.enableMouseKeyboard(False)
	for i in range(3):
		keypress('<alt>')
		keypress('<left>')
		time.sleep(0.3)
		keyrelease('<alt>')
		keyrelease('<left>')
                print '==============='
		time.sleep(1)
	time.sleep(2)
	g_sst.scrprint(g_tag,'LastMusic',g_currentPath)
        sourceobj.enableMouseKeyboard(True)
	return (True)
def NextBtn_cos64():
	print('NextMusic')
        sourceobj.enableMouseKeyboard(False)
	for i in range(2):
		keypress('<alt>')
		keypress('<right>')
		time.sleep(0.3)
		keyrelease('<alt>')
		keyrelease('<right>')
                print'-----------------'
		time.sleep(1)
	time.sleep(2)
	g_sst.scrprint(g_tag,'NextMusic',g_currentPath)
        sourceobj.enableMouseKeyboard(True)
	return (True)
def maxMusic_cos64():
	print('maxWindow....')
	sourceobj.enableMouseKeyboard(True)
	keypress('<f11>')
	keyrelease('<f11>')
	time.sleep(1)
	keypress('<f11>')
	keyrelease('<f11>')
	time.sleep(2)
        g_sst.scrprint(g_tag,'Maxwindow',g_currentPath)
        sourceobj.enableMouseKeyboard(True)
	return (True)

def closeMusic_cos64():
	print ('closewindow.....')
	keypress('<ctrl>')
	keypress('q')
	time.sleep(1)
	keyrelease('<ctrl>')
	keyrelease('q')

	return (True)

def main():
    print g_osName
    if g_osName == 'cos':
	print ('OS %s ready for opening media')%(g_osName)

    name = ""
    addsourcefile(media_dir)
    if 1 == OpenMedia_cos64(media_dir,music_tool):
        print('open already')
    else:
   	print('Error to open music')
        os.system('killall ' + music_tool)
    PauseAndPlay_cos64()
    NextBtn_cos64()
    LastestBtn_cos64()
    maxMusic_cos64()
	
    if g_s3 == 1:
        os.system('echo '+passwd+' | sudo -S rtcwake -m mem -m 60')
	g_sst.scrprint('1.5.2-AudioAndVideoPlay','PauseMusic',g_currentPath)
    else:
	g_log.wlog(g_tag,'os not S3')
	if g_s4 == 1:
	    os.system('echo '+passwd+' | sudo -S rtcwake -m disk -m 60')
    	    g_sst.scrprint(g_tag,'PauseMusic',g_currentPath)
	else:
	    g_log.wlog(g_tag,'os not S4')
	
    time.sleep(5)
    os.system('killall ' + music_tool)
    time.sleep(3)
    umountSourceFile(media_dir)
    return

if __main__ == "__main__":
    main()
