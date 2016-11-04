#coding=utf-8
__main__="__main__"

from ldtp import *
from ldtputils import *
from multiprocessing import Process
import time
import os
import logging
import sys
import string
import signal
import getpass
import subprocess
import platform

reload(sys)
sys.setdefaultencoding("utf8")

g_currentPath = sys.path[0]
sys.path.append(os.environ['AUTOTEST_PUBLIC_LIB'])

g_s4 = int(os.environ['S4_ENABLE'])
print "s4 enable is "
print g_s4

g_s3 = int(os.environ['S3_ENABLE'])
print "s3 enable is "
print g_s3

videodir = '/resource/'

if not os.path.exists(g_currentPath + videodir):
    os.system('mkdir -p '+ g_currentPath + videodir)

if os.path.exists(g_currentPath + videodir+'xrandr.txt'):
	os.system('rm -rf '+ g_currentPath + videodir+'xrandr.txt')

from logcase import Logcase
from caseobject import CaseObject
g_log = Logcase()
g_tag = 'video_scan_log'
picobj = CaseObject('1.3.2.2-VideoScan',g_currentPath + '/1.3.2.2-VideoScan.xml')
doc = picobj.getDocumentNode()
g_osName = picobj.getOSName()

from screenshot import Screenshot
g_sst = Screenshot()

from ldtppub import LDTPPub
g_ldtpObj = LDTPPub()

common_node = picobj.getXMLNode(doc,'common',0)
count_node = picobj.getXMLNode(common_node, 'count', 0)
count = picobj.getXMLNodeValue(count_node, 0)
print count

data_node = picobj.getXMLNode(doc,'data',0)


video_source = picobj.getXMLNode(data_node, 'video_source_name', 0)
video_source_name = picobj.getXMLNodeValue(video_source, 0)
print video_source_name

video_source1 = picobj.getXMLNode(data_node, 'video_source_name1', 0)
video_source_name1 = picobj.getXMLNodeValue(video_source1, 0)
print video_source_name1

video_source2 = picobj.getXMLNode(data_node, 'video_source_name2', 0)
video_source_name2 = picobj.getXMLNodeValue(video_source2, 0)
print video_source_name2

video_source3 = picobj.getXMLNode(data_node, 'video_source_name3', 0)
video_source_name3 = picobj.getXMLNodeValue(video_source3, 0)
print video_source_name3

video_source4 = picobj.getXMLNode(data_node, 'video_source_name4', 0)
video_source_name4 = picobj.getXMLNodeValue(video_source4, 0)
print video_source_name4


password = picobj.getPasswd()
print (password)

pcusername=getpass.getuser()
print pcusername

g_tag = '1.3.2.2-VideoScan'
g_install = os.environ['AUTOTEST_DIR']

def change_pixel():
	os.system('xrandr | grep \* | awk \'{print $1}\' > ' + g_currentPath + '/resource/xrandr.txt')
	   
        with open(g_currentPath + '/resource/xrandr.txt', 'r') as xrandrFile:
            fileBuffer = xrandrFile.read()
	pixelList = fileBuffer.strip().split('x')
	print pixelList

	os.system('xrandr  | grep [0-9][0-9][0-9]x[0-9][0-9][0-9] | grep -v [a-w][w-z] | awk \'{print $1}\'  > ' + g_currentPath + '/resource/allxrandr.txt')
	with open(g_currentPath + '/resource/allxrandr.txt', 'r') as allxrandrFile:
		xrandrlist = allxrandrFile.readlines()
		count = len(open(g_currentPath + '/resource/allxrandr.txt', 'r').readlines())
		print "*******************"
		print count
				
	for i in range(1,count):
		onexrandr = xrandrlist[i].strip().split('x')
		print onexrandr
		wide = onexrandr[0]
		high = onexrandr[1]
		g_ldtpObj.setResolution(g_osName, wide, high)
		time.sleep(4)
    		if guiexist(u'dlg\u9519\u8bef') == 1:
    			return	
		g_sst.scrprint('1.3.2.2-VideoScan',wide+'x'+high,g_currentPath)
					
	g_ldtpObj.setResolution(g_osName, pixelList[0], pixelList[1])
	time.sleep(4)
	g_sst.scrprint('1.3.2.2-VideoScan','best pixel',g_currentPath)
	return

def openVideo_kylin(tran_dir):
    g_log.ilog(g_tag,'opening')
    print "open video..."
    print tran_dir
    os.system('smplayer '+tran_dir+' &')
    time.sleep(3) 	
    print "open video finish..."
    return

def scanVideo_kylin():
    g_log.ilog(g_tag,'Is editing video')
    print ('Is scaning video')
    time.sleep(3)
    #Voice
    print ('up voice start')
    for a in range(0,5):
	up = chr(48)
    	keypress('<'+up+'>')
    	keyrelease('<'+up+'>')
    	time.sleep(1)
    print ('up voice end')
    
    os.system('killall firefox')
    
    g_sst.scrprint('1.3.2.2-VideoScan','voice up',g_currentPath)

    print ('down voice start')
    for a in range(0,1):
        down = chr(57)
    	keypress('<'+down+'>')
    	keyrelease('<'+down+'>')
    	time.sleep(1)
    print ('down voice end')
    g_sst.scrprint('1.3.2.2-VideoScan','voice down',g_currentPath)
    #Progress 
    print ('Progress increase')
    for a in range(0,2):
    	keypress('<up>')
    	keyrelease('<up>')
    	time.sleep(2)

    g_sst.scrprint('1.3.2.2-VideoScan','progress increase',g_currentPath)
    print ('Progress decrease')
    #for a in range(0,2):
    #	keypress('<down>')
    #	keyrelease('<dowm>')
    #	time.sleep(2)
    if g_s3 == 1:
    	os.system('echo '+password+' | sudo -S rtcwake -m mem -s 120')
    	time.sleep(10)
    	g_sst.scrprint('1.3.2.2-VideoScan','S3',g_currentPath)
    else:
	g_log.wlog(g_tag,'os not S3')

    if g_s4 == 1:
    	os.system('echo '+password+' | sudo -S rtcwake -m disk -s 120')
    	g_sst.scrprint('1.3.2.2-VideoScan','S4',g_currentPath)
    else:
	g_log.wlog(g_tag,'os not S4')	
    return

def maxWindow_kylin():
    print ('maxwindow')
    maxwindow = chr(102)
    keypress('<'+maxwindow+'>')
    keyrelease('<'+maxwindow+'>')
    time.sleep(3)
    g_sst.scrprint('1.3.2.2-VideoScan','maxwindow',g_currentPath)

    return

def closeWindow_kylin():
    print ('close window .....')
    os.system('killall smplayer')	
    return

	
def openVideo_cos(tran_dir):
    g_log.ilog(g_tag,'opening')
    print "open video..."
    print tran_dir
    os.system('totem '+tran_dir+' &')
    time.sleep(3) 
    if guiexist(u'dlg\u9519\u8bef') == 1:
	
    	return	
	
    print "open video finish..."
    return

def scanVideo_cos():
    g_log.ilog(g_tag,'Is editing video')
    print ('Is scaning video')

    time.sleep(3)
    if guiexist(u'dlg\u9519\u8bef') == 1:
    	return
    for a in range(0,5):
    	keypress('<down>')
    	keyrelease('<down>')
    	time.sleep(1)
	if guiexist(u'dlg\u9519\u8bef') == 1:
		
    		return
    print ('down voice end')
    g_sst.scrprint('1.3.2.2-VideoScan','voice down',g_currentPath)

    for a in range(0,4):
    	keypress('<up>')
    	keyrelease('<up>')
    	time.sleep(1)
	if guiexist(u'dlg\u9519\u8bef') == 1:
		
    		return
    print ('up voice end')
    g_sst.scrprint('1.3.2.2-VideoScan','voice up',g_currentPath)

    #Progress 
    print ('Progress increase')
    for a in range(0,2):
    	keypress('<right>')
    	keyrelease('<right>')
    	time.sleep(2)
	if guiexist(u'dlg\u9519\u8bef') == 1:
    		return
    g_sst.scrprint('1.3.2.2-VideoScan','progress increase',g_currentPath)

    print ('Progress decrease')
    for a in range(0,2):
    	keypress('<left>')
    	keyrelease('<left>')
    	time.sleep(2)
	if guiexist(u'dlg\u9519\u8bef') == 1:
    		return
    g_sst.scrprint('1.3.2.2-VideoScan','progress decrease',g_currentPath)

    if g_s3 == 1:
    	os.system('echo '+password+' | sudo -S rtcwake -m mem -s 120')
    	time.sleep(10)
    	g_sst.scrprint('1.3.2.2-VideoScan','S3',g_currentPath)
    else:
	g_log.wlog(g_tag,'os not S3')

    if guiexist(u'dlg\u9519\u8bef') == 1:
    	return

    if g_s4 == 1:
    	os.system('echo '+password+' | sudo -S rtcwake -m disk -s 120')
    	g_sst.scrprint('1.3.2.2-VideoScan','S4',g_currentPath)
    else:
	g_log.wlog(g_tag,'os not S4')

    print ('edit end ...')
    return

def maxWindow_cos(name):
    print ('maxwindow')
    if guiexist(u'dlg\u9519\u8bef') != 1:
	print name
    	maximizewindow(name)
	g_sst.scrprint('1.3.2.2-VideoScan','maxwindow',g_currentPath)
    else:   
    	return
    
    time.sleep(3)
    return

def closeWindow_cos():
    print ('close window .....')    
    os.system('killall totem')	
    return

def getCmdResult(cmd):
	process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(o, e) = process.communicate()
	return o.strip()

   
def main():
	if platform.architecture()[0] == "64bit":
		name = ""
		videospacename =''
		for i in range(0, 5):
			if i == 0:
				tran_dir = os.path.expanduser(video_source_name)
				print tran_dir
				print '0*******'
				name = os.path.basename(tran_dir)
				print name
				if not os.path.exists(tran_dir):
    					g_log.ilog(g_tag,'video resource not exist')
					print ('not exist video source')
					continue	
			elif i == 1:
				tran_dir = os.path.expanduser(video_source_name1)
				print tran_dir
				print '1*******'
				name = os.path.basename(tran_dir)
				print name
				if not os.path.exists(tran_dir):
    					g_log.ilog(g_tag,'video resource not exist')
					print ('not exist video source')
					continue
			elif i == 2:
				tran_dir = os.path.expanduser(video_source_name2)
				print tran_dir
				print '2*******'
				name = os.path.basename(tran_dir)
				print name
				if not os.path.exists(tran_dir):
    					g_log.ilog(g_tag,'video resource not exist')
					print ('not exist video source')
					continue	
			elif i == 3:
				tran_dir = os.path.expanduser(video_source_name3)
				print tran_dir
				print '3*******'
				name = os.path.basename(tran_dir)
				print name
				if not os.path.exists(tran_dir):
    					g_log.ilog(g_tag,'video resource not exist')
					print ('not exist video source')
					continue
			elif i == 4:
				tran_dir = os.path.expanduser(video_source_name4)
				print tran_dir
				print '4*******'
				name = os.path.basename(tran_dir)
				print name
				if not os.path.exists(tran_dir):
    					g_log.ilog(g_tag,'video resource not exist')
					print ('not exist video source')
					continue

         		if len(name.split(' ')) > 1:
				for videoname in name.split(' '):
					videospacename += videoname + '\\' + ' '
				name = videospacename[:-2]
				print name
				os.path.dirname(tran_dir)
				tran_dir = os.path.dirname(tran_dir) +'/'+ name
				print tran_dir
				videospacename = ''
			else:
				pass
			print name
	
            		openVideo_kylin(tran_dir)
	    		#picobj.enableMouseKeyboard(False)
            		scanVideo_kylin()
	    		maxWindow_kylin()
			time.sleep(2)
	    		#picobj.enableMouseKeyboard(True)
	    		change_pixel()
			if i == 0:
	    			#change_pixel()
	    			os.system(g_currentPath+videodir+'resolution_rotate.sh')
				pass
            		print ('conti.....')
	    		#picobj.enableMouseKeyboard(False)
            		closeWindow_kylin()
			time.sleep(5)
	    		#picobj.enableMouseKeyboard(True)
        	return

	if platform.architecture()[0] == "32bit":
		cmd = 'dpkg -l | grep gstreamer1.0-plugins-ugly | awk \'{print $1}\''
		if g_osName == 'cos' and getCmdResult(cmd) != 'ii':
			print "is installing codec-debs"
			os.chdir(g_install+'/tools/build116a-codec-debs')
			os.system('echo '+password+' | sudo -S ./install.sh')
			os.chdir(g_currentPath)
			print "install finish"
			
		name = ""
		videospacename =''
		for i in range(0, 5):
			if i == 0:
				tran_dir = os.path.expanduser(video_source_name)
				print tran_dir
				print '0*******'
				name = os.path.basename(tran_dir)
				print name
				if not os.path.exists(tran_dir):
    					g_log.ilog(g_tag,'video resource not exist')
					print ('not exist video source')
					continue	
			elif i == 1:
				tran_dir = os.path.expanduser(video_source_name1)
				print tran_dir
				print '1*******'
				name = os.path.basename(tran_dir)
				print name
				if not os.path.exists(tran_dir):
    					g_log.ilog(g_tag,'video resource not exist')
					print ('not exist video source')
					continue
			elif i == 2:
				tran_dir = os.path.expanduser(video_source_name2)
				print tran_dir
				print '2*******'
				name = os.path.basename(tran_dir)
				print name
				if not os.path.exists(tran_dir):
    					g_log.ilog(g_tag,'video resource not exist')
					print ('not exist video source')
					continue	
			elif i == 3:
				tran_dir = os.path.expanduser(video_source_name3)
				print tran_dir
				print '3*******'
				name = os.path.basename(tran_dir)
				print name
				if not os.path.exists(tran_dir):
    					g_log.ilog(g_tag,'video resource not exist')
					print ('not exist video source')
					continue
			elif i == 4:
				tran_dir = os.path.expanduser(video_source_name4)
				print tran_dir
				print '4*******'
				name = os.path.basename(tran_dir)
				print name
				if not os.path.exists(tran_dir):
    					g_log.ilog(g_tag,'video resource not exist')
					print ('not exist video source')
					continue

         		if len(name.split(' ')) > 1:
				for videoname in name.split(' '):
					videospacename += videoname + '\\' + ' '
				name = videospacename[:-2]
				print name
				os.path.dirname(tran_dir)
				tran_dir = os.path.dirname(tran_dir) +'/'+ name
				print tran_dir
				videospacename = ''
			else:
				pass
			print name

            		openVideo_cos(tran_dir)
			if guiexist(u'dlg\u9519\u8bef') == 1:
				g_sst.scrprint('1.3.2.2-VideoScan','Conventional flow error',g_currentPath)
				os.system('killall totem')
				continue
			time.sleep(3)
            		scanVideo_cos()
			if guiexist(u'dlg\u9519\u8bef') == 1:
				g_sst.scrprint('1.3.2.2-VideoScan','Conventional flow error',g_currentPath)
				os.system('killall totem')
				continue
	    		maxWindow_cos(name)
			if guiexist(u'dlg\u9519\u8bef') == 1:
				g_sst.scrprint('1.3.2.2-VideoScan','Conventional flow error',g_currentPath)
				os.system('killall totem')
				continue

			if g_osName == 'cos':
				g_log.ilog(g_tag,'not setResolution ')
			if g_osName == 'isoft':
				change_pixel()

			if guiexist(u'dlg\u9519\u8bef') == 1:
				g_sst.scrprint('1.3.2.2-VideoScan','Conventional flow error',g_currentPath)
				os.system('killall totem')
				continue
			if i == 0:
				print ("start run resolution_rotate.sh")
				#change_pixel()
				os.system(g_currentPath+videodir+'resolution_rotate.sh')
			
			time.sleep(5)
			if guiexist(u'dlg\u9519\u8bef') == 1:
				g_sst.scrprint('1.3.2.2-VideoScan','Conventional flow error',g_currentPath)
				os.system('killall totem')
				continue
			closeWindow_cos()
			time.sleep(3)
            		print ('conti.....')


            	return

            


if __main__=="__main__":
    main()
