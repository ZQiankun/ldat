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

g_s4 = int(os.environ['S4_ENABLE'])
print "s4 enable is "
print g_s4

g_s3 = int(os.environ['S3_ENABLE'])
print "s3 enable is "
print g_s3

picdir = '/resource/'

if not os.path.exists(g_currentPath + picdir):
	os.system('mkdir -p '+ g_currentPath + picdir)

if os.path.exists(g_currentPath + picdir+'xrandr.txt'):
	os.system('rm -rf '+ g_currentPath + picdir+'xrandr.txt')

from logcase import Logcase
from caseobject import CaseObject
g_log = Logcase()

picobj = CaseObject('1.3.2.1-PictureEdit',g_currentPath + '/1.3.2.1-PictureEdit.xml')
doc = picobj.getDocumentNode()
g_osName = picobj.getOSName()

from screenshot import Screenshot
g_sst = Screenshot()

from ldtppub import LDTPPub
g_ldtpObj = LDTPPub()

common_node = picobj.getXMLNode(doc,'common',0)
count_node = picobj.getXMLNode(common_node, 'count', 0)
count = picobj.getXMLNodeValue(count_node, 0)

data_node = picobj.getXMLNode(doc,'data',0)
picture_source = picobj.getXMLNode(data_node, 'picture_source_name', 0)
picture_source_name = picobj.getXMLNodeValue(picture_source, 0)

picture_source1 = picobj.getXMLNode(data_node, 'picture_source_name1', 0)
picture_source_name1 = picobj.getXMLNodeValue(picture_source1, 0)

picture_source2 = picobj.getXMLNode(data_node, 'picture_source_name2', 0)
picture_source_name2 = picobj.getXMLNodeValue(picture_source2, 0)

picture_source3 = picobj.getXMLNode(data_node, 'picture_source_name3', 0)
picture_source_name3 = picobj.getXMLNodeValue(picture_source3, 0)

picture_source4 = picobj.getXMLNode(data_node, 'picture_source_name4', 0)
picture_source_name4 = picobj.getXMLNodeValue(picture_source4, 0)


password = picobj.getPasswd()
print (password)

def openPicture(name):
	print ('opening')
	g_log.ilog('1.3.2.1-PictureEdit','opening') 
	if not os.path.exists(g_currentPath+picdir+name):
		print('picturn not in resource')
		return
	os.system('eog '+g_currentPath+picdir+name+' &')
	time.sleep(3)
	return

def openPicture_kylin(name):
	print ('opening')
	g_log.ilog('1.3.2.1-PictureEdit','opening') 
	if not os.path.exists(g_currentPath+picdir+name):
		print('picturn not in resource')
		return
	os.system('eom '+g_currentPath+picdir+name+' &')
	time.sleep(3)
	return

def openPicture_isoft(name):
	print ('opening')
	g_log.ilog('1.3.2.1-PictureEdit','opening') 
	if not os.path.exists(g_currentPath+picdir+name):
		print('picturn not in resource')
		return
	os.system('gthumb '+g_currentPath+picdir+name+' &')
	time.sleep(3)
	return

def editPicture(name):
	print ('Is editing picture')
	g_log.ilog('1.3.2.1-PictureEdit','Is editing picture')
	if not os.path.exists(g_currentPath+picdir+name):
		print('picturn not in resource')
		return
	time.sleep(2)

	print ('clockwise')
	clockwise = click(name,'btn顺时针')
	time.sleep(2)
	g_sst.scrprint('1.3.2.1-PictureEdit','clockwise',g_currentPath)

	print ('anticlockwise')
	anticlockwise = click(name,'btn逆时针')
	time.sleep(2)
	g_sst.scrprint('1.3.2.1-PictureEdit','anticlockwise',g_currentPath)

	print ('magnification')
	for d in range(0,3):
		magnification = click(name,'btn放大')
		time.sleep(2)
	g_sst.scrprint('1.3.2.1-PictureEdit','magnification',g_currentPath)

	print ('narrow')
	for e in range(0,2):
		narrow = click(name,'btn缩小')
		time.sleep(2)
	g_sst.scrprint('1.3.2.1-PictureEdit','narrow',g_currentPath)
	
	if g_s3 == 1:
		os.system('echo '+password+' | sudo -S rtcwake -m mem -s 120')
		g_sst.scrprint('1.3.2.1-PictureEdit','S3',g_currentPath)
	else:
		g_log.wlog('1.3.2.1-PictureEdit','os not S3')

	if g_s4 == 1:
		time.sleep(10)
		os.system('echo '+password+' | sudo -S rtcwake -m disk -s 120')
		g_sst.scrprint('1.3.2.1-PictureEdit','S4',g_currentPath)
	else:
		g_log.wlog('1.3.2.1-PictureEdit','os not S4')
		
	return

def editPicture_kylin(name):
	print ('Is editing picture')
	g_log.ilog('1.3.2.1-PictureEdit','Is editing picture')
	if not os.path.exists(g_currentPath+picdir+name):
		print('picturn not in resource')
		return
	time.sleep(2)

	print ('clockwise')
	keypress('<ctrl>')
	keypress('r')
	keyrelease('<ctrl>')
	keyrelease('r')
	time.sleep(2)
	g_sst.scrprint('1.3.2.1-PictureEdit','clockwise',g_currentPath)

	print ('anticlockwise')
	keypress('<alt>')
	keypress('e')
	keyrelease('<alt>')
	keyrelease('e')
	time.sleep(2)
	keypress('l')
	keyrelease('l')
	time.sleep(2)
	g_sst.scrprint('1.3.2.1-PictureEdit','anticlockwise',g_currentPath)

	print ('magnification')
	for d in range(0,3):
		keypress('<ctrl>')
		keypress('+')
		keypress('+')
		keyrelease('<ctrl>')
		keyrelease('+')
		keyrelease('+')
		time.sleep(2)
	g_sst.scrprint('1.3.2.1-PictureEdit','magnification',g_currentPath)

	print ('narrow')
	for e in range(0,2):
		keypress('<ctrl>')
		keypress('-')
		keypress('-')
		keyrelease('<ctrl>')
		keyrelease('-')
		keyrelease('-')
		time.sleep(2)
	g_sst.scrprint('1.3.2.1-PictureEdit','narrow',g_currentPath)

	if g_s3 == 1:	
		os.system('echo '+password+' | sudo -S rtcwake -m mem -s 120')
		g_sst.scrprint('1.3.2.1-PictureEdit','S3',g_currentPath)
	else:
		g_log.wlog('1.3.2.1-PictureEdit','os not S3')

	if g_s4 == 1:
		time.sleep(10)
		os.system('echo '+password+' | sudo -S rtcwake -m disk -s 120')
		g_sst.scrprint('1.3.2.1-PictureEdit','S4',g_currentPath)
	else:
		g_log.wlog('1.3.2.1-PictureEdit','os not S4')
		
	return

def editPicture_isoft(name):
	print ('Is editing picture')
	g_log.ilog('1.3.2.1-PictureEdit','Is editing picture')
	if not os.path.exists(g_currentPath+picdir+name):
		print('picturn not in resource')
		return
	time.sleep(2)

	print ('clockwise')
	
	keypress('r')
	keyrelease('r')
	time.sleep(2)
	g_sst.scrprint('1.3.2.1-PictureEdit','clockwise',g_currentPath)

	print ('anticlockwise')
	keypress('<shift>')
	keypress('r')
	keyrelease('<shift>')
	keyrelease('r')
	time.sleep(2)
	g_sst.scrprint('1.3.2.1-PictureEdit','anticlockwise',g_currentPath)
	
	print ('magnification')
	for d in range(0,3):
		keypress('+')
		keyrelease('+')
		time.sleep(2)
	g_sst.scrprint('1.3.2.1-PictureEdit','magnification',g_currentPath)

	print ('narrow')
	for e in range(0,2):
		keypress('-')
		keyrelease('-')
		time.sleep(2)
	g_sst.scrprint('1.3.2.1-PictureEdit','narrow',g_currentPath)
	
	if g_s3 == 1:	
		os.system('echo '+password+' | sudo -S rtcwake -m mem -s 120')
		g_sst.scrprint('1.3.2.1-PictureEdit','magnification',g_currentPath)
	else:
		g_log.wlog('1.3.2.1-PictureEdit','os not S3')	
	if g_s4 == 1:
		time.sleep(10)
		os.system('echo '+password+' | sudo -S rtcwake -m disk -s 120')
		g_sst.scrprint('1.3.2.1-PictureEdit','magnification',g_currentPath)
	else:
		g_log.wlog('1.3.2.1-PictureEdit','os not S4')
		
	return

def maxWindow(name):
	print ('maxwindow.....')
	if not os.path.exists(g_currentPath+picdir+name):
		print('picturn not in resource')
		return
	maximizewindow(name)
	time.sleep(3)
	return

def maxWindow_kylin(name):
	print ('maxwindow.....')
	if not os.path.exists(g_currentPath+picdir+name):
		print('picturn not in resource')
		return
	keypress('f11')
	keyrelease('f11')
	time.sleep(3)
	keypress('f11')
	keyrelease('f11')
	time.sleep(2)
	return

def maxWindow_isoft(name):
	print ('maxwindow.....')
	if not os.path.exists(g_currentPath+picdir+name):
		print('picturn not in resource')
		return
	maximizewindow(name+'*')
	time.sleep(3)
	return


def minWindow(name):
	print ('minwindow.....')
	if not os.path.exists(g_currentPath+picdir+name):
		print('picturn not in resource')
		return
	minimizewindow(name)
	time.sleep(3)
	return

def minWindow_isoft(name):
	print ('minwindow.....')
	if not os.path.exists(g_currentPath+picdir+name):
		print('picturn not in resource')
		return
	minimizewindow(name+'*')
	time.sleep(3)
	return

def closeWindow(name):
	print ('closewindow.....')
	if not os.path.exists(g_currentPath+picdir+name):
		print('picturn not in resource')
		return
	closewindow(name)

	return

def closeWindow_kylin(name):
	print ('closewindow.....')
	if not os.path.exists(g_currentPath+picdir+name):
		print('picturn not in resource')
		return
	keypress('<ctrl>')
	keypress('w')
	keyrelease('<ctrl>')
	keyrelease('w')

	return

def closeWindow_isoft(name):
	print ('closewindow.....')
	if not os.path.exists(g_currentPath+picdir+name):
		print('picturn not in resource')
		return
	closewindow(name+'*')

	return

def save(name):
	if not os.path.exists(g_currentPath+picdir+name):
		print('picturn not in resource')
		return
	picobj.enableMouseKeyboard(False)

	if name.find('.gif') == -1:
		keypress('<alt>')
		keypress('s')
		keyrelease('<alt>')
		keyrelease('s')
	else:
		keypress('<alt>')
		keypress('w')
		keyrelease('<alt>')
		keyrelease('w')
	
	picobj.enableMouseKeyboard(True)

	return

def save_kylin(name):
	if not os.path.exists(g_currentPath+picdir+name):
		print('picturn not in resource')
		return
	picobj.enableMouseKeyboard(False)

	keypress('<alt>')
	keypress('s')
	keyrelease('<alt>')
	keyrelease('s')
	
	picobj.enableMouseKeyboard(True)

	return

def save_isoft(name):
	if not os.path.exists(g_currentPath+picdir+name):
		print('picturn not in resource')
		return
	picobj.enableMouseKeyboard(False)

	if name.find('.gif') != -1:
		keypress('<alt>')
		keypress('n')
		keyrelease('<alt>')
		keyrelease('n')

	elif name.find('.bmp') != -1:
		keypress('<alt>')
		keypress('n')
		keyrelease('<alt>')
		keyrelease('n')
	else:
		keypress('<alt>')
		keypress('s')
		keyrelease('<alt>')
		keyrelease('s')
	
	picobj.enableMouseKeyboard(True)

	return
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
		g_sst.scrprint('1.3.2.1-PictureEdit',wide+'x'+high,g_currentPath)
					
	g_ldtpObj.setResolution(g_osName, pixelList[0], pixelList[1])
	time.sleep(4)
	g_sst.scrprint('1.3.2.1-PictureEdit','best pixel',g_currentPath)
	return

def kylin_version():
	kylinSysVersion = '/etc/issue'
	with open(kylinSysVersion,'r') as systemFile:
		fileBuffer = systemFile.read()
		if fileBuffer.find('6.0') != -1:
			return 'kylin 6.0'
		elif fileBuffer.find('4.0') != -1:
			return 'kylin 4.0'
def main():
	print g_osName		
	if g_osName == 'cos' or kylin_version() == 'kylin 6.0':
		if g_osName == 'cos':
			print ('this is cos')
		elif kylin_version() == 'kylin 6.0':
			print ('this is  kylin 6.0')

		name = ""
		for i in range(0, 5):
			if i == 0:
				name = picture_source_name	
			elif i == 1:
				name = picture_source_name1		
			elif i == 2:
				name = picture_source_name2		
			elif i == 3:
				name = picture_source_name3
			elif i == 4:
				name = picture_source_name4
				
			print name
			openPicture(name)
			editPicture(name)
			maxWindow(name)
			if kylin_version() == 'kylin 6.0':
				change_pixel()

		time.sleep(3)
                click(name,'mnu幻灯片放映(L)')
		time.sleep(20)
		os.system('killall eog')	

		
		return

	elif kylin_version() == 'kylin 4.0' or g_osName == 'kylin-V4':
		name = ""
		for i in range(0, 5):
			if i == 0:
				name = picture_source_name
				openPicture_kylin(name)	
			elif i == 1:
				name = picture_source_name1
				openPicture_kylin(name)
			elif i == 2:
				name = picture_source_name2
				openPicture_kylin(name)		
			elif i == 3:
				name = picture_source_name3
				openPicture_kylin(name)
			elif i == 4:
				name = picture_source_name4
				openPicture_kylin(name)
				
			print name
			
			editPicture_kylin(name)
			maxWindow_kylin(name)
			change_pixel()			


			
		time.sleep(5)
		os.system('killall eom')	

		
		return
	
	elif g_osName == 'isoft':
		print ('this is isoft')

		name = ""
		for i in range(0, 5):
			if i == 0:
				name = picture_source_name	
			elif i == 1:
				name = picture_source_name1		
			elif i == 2:
				name = picture_source_name2		
			elif i == 3:
				name = picture_source_name3
			elif i == 4:
				name = picture_source_name4
				
			print name
			openPicture_isoft(name)
			editPicture_isoft(name)
			maxWindow_isoft(name)
			change_pixel()		


		time.sleep(5)
		os.system('killall gthumb')	
		return

if __main__=="__main__":
	main()
