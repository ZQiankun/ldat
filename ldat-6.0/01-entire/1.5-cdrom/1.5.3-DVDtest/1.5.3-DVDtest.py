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


g_tag = '1.5.3-DVDtest'
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
video_tool = 'smplayer'

from logcase import Logcase
from caseobject import CaseObject
g_log = Logcase()

sourceobj = CaseObject(g_tag,g_currentPath + '/1.5.3-DVDtest.xml')
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
    cdpath = "mount | grep 'iso9660\|udf' | awk '{print $1}'"
    print '==========%s======='%(cdpath)
    process = subprocess.Popen(cdpath,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    (o,e)=process.communicate()
    devName = o.strip()
    print('-------------add %s----')%(devName)
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
                if (files.endswith('wav') or files.endswith('mp4') or
                    files.endswith('avi') or files.endswith('rmvb') or
                    files.endswith('mkv') or files.endswith('mov') or
                    files.endswith('mpg')):
                    print ('**********[ %s ]************')%(files)
                    video_source_name.append(files)
                    if len(video_source_name) == None:
                        g_log.wlog('no video source files found')
		        print ('no video found')
                        return
	return 

###################################################
# video in cdrom for smplayer
##################################################
def OpenMedia_cos64(src_dir,tools):
	print ('opening source')
	g_log.ilog(g_tag,'opening')
	os.system(tools+' ' + g_currentPath +src_dir +' &')
	time.sleep(4)
	os.system('killall firefox')
	return (True)

def pauseVideo():
        sourceobj.enableMouseKeyboard(False)
	print('PauseVideo')
	keypress(' ')
	keyrelease(' ')
	time.sleep(1)
        keypress(' ')
	keyrelease(' ')
	time.sleep(1)
	g_sst.scrprint(g_tag,'PauseVideo',g_currentPath)
	sourceobj.enableMouseKeyboard(True)
	return (True)

def editVideo_cos64():
	print('Is editing video')
	g_log.ilog(g_tag,'Is editing video')
	if not os.path.exists(g_currentPath + media_dir):
		print('video not in the resource')
		return  
	time.sleep(4)
        sourceobj.enableMouseKeyboard(False)

	print('NextVideo')
	keypress('<shift>')
        keypress('<.>')
	keyrelease('<shift>')
        keyrelease('<.>')
	time.sleep(3)
	g_sst.scrprint(g_tag,'NextVideo',g_currentPath)

	print('FastForward_S')
	keypress('<right>')
	keyrelease('<right>')
	time.sleep(1)
	g_sst.scrprint(g_tag,'FastForward',g_currentPath)

	print('FastBackward_S')
	keypress('<left>')
	keyrelease('<left>')
	time.sleep(1)
	g_sst.scrprint(g_tag,'FastBackward',g_currentPath)
	
	print('FastForward_M')
	keypress('<up>')
	keyrelease('<up>')
	time.sleep(1)
	g_sst.scrprint(g_tag,'FastForward',g_currentPath)

	print('FastBackward_M')
	keypress('<down>')
	keyrelease('<down>')
	time.sleep(1)
	g_sst.scrprint(g_tag,'FastBackward',g_currentPath)
	

        '''	
        print('FastForward_TM')
        keypress('<pgUp>')
   	keyrelease('<pgUp>')
	time.sleep(1)
	g_sst.scrprint(g_tag,'FastForward',g_currentPath)

        print('FastBackward_TM')
	keypress('<pgDown>')
	keyrelease('<pgDown>')
	time.sleep(2)
        g_sst.scrprint(g_tag,'FastBackward',g_currentPath)
   	'''
	print('LastVideo')
	keypress('<shift>')
        keypress('<,>')
	keyrelease('<shift>')
        keyrelease('<,>')
	time.sleep(3)
	g_sst.scrprint(g_tag,'LastVideo',g_currentPath)
        sourceobj.enableMouseKeyboard(True)
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
	
	return (True)

def fullScreen_cos64():
    
	print('FullScreen')
	keypress('f')
	keyrelease('f')
	time.sleep(4)
	keypress('f')
	keyrelease('f')
	g_sst.scrprint(g_tag,'FullScreen',g_currentPath)

	return (True)


def main():
    print g_osName
    if g_osName == 'cos':
	print ('OS %s ready for opening media')%(g_osName)

    name = ""
    addsourcefile( media_dir)
    if True == OpenMedia_cos64(media_dir,video_tool):
    	print('testing video successfully!!!')
    else:
        print('ERROR to open video')
   	os.system('killall ' + video_tool)
        umountSourceFile(media_dir)
    pauseVideo()
    if True ==editVideo_cos64():
        print('editVideo_cos64 successfully')
    else:
        g_log.wlog('editVideo_cos64 ERROR')
        os.system('killall ' + video_tool)
        umountSourceFile(media_dir)
    fullScreen_cos64()
    time.sleep(5)
    os.system('killall ' + video_tool)
    time.sleep(3)
    umountSourceFile(media_dir)
    return

if __main__ == "__main__":
    main()
