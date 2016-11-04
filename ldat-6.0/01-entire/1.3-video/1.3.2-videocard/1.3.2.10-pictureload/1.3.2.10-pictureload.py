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
picres = '/result/'

if not os.path.exists(g_currentPath + picdir):
	os.system('mkdir -p '+ g_currentPath + picdir)

if os.path.exists(g_currentPath + picdir+'xrandr.txt'):
	os.system('rm -rf '+ g_currentPath + picdir+'xrandr.txt')

from logcase import Logcase
from caseobject import CaseObject
g_log = Logcase()

picobj = CaseObject('1.3.2.10-pictureload',g_currentPath + '/1.3.2.10-pictureload.xml')
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


password = picobj.getPasswd()
print (password)

def openPicture(name):
	print ('opening')
	g_log.ilog('1.3.2.10-pictureload','opening') 
	if not os.path.exists(g_currentPath+picdir+name):
		print('picturn not in resource')
		return
	os.system('eog '+g_currentPath+picdir+name+' &')
	time.sleep(3)
	return

def openPicture_kylin(name):
	print ('opening')
	g_log.ilog('1.3.2.10-pictureload','opening') 
	if not os.path.exists(g_currentPath+picdir+name):
		print('picturn not in resource')
		return
	os.system('eom '+g_currentPath+picdir+name+' &')
	time.sleep(3)
	return

def openPicture_isoft(name):
	print ('opening')
	g_log.ilog('1.3.2.10-pictureload','opening') 
	if not os.path.exists(g_currentPath+picdir+name):
		print('picturn not in resource')
		return
	os.system('gthumb '+g_currentPath+picdir+name+' &')
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
	if g_osName == 'ubuntu' or g_osName == 'cos' or kylin_version() == 'kylin 6.0':
		if g_osName == 'cos':
			print ('this is cos')
		elif kylin_version() == 'kylin 6.0':
			print ('this is  kylin 6.0')

		name = ""
		for i in range(0, 3):
			if i == 0:
				name = picture_source_name	
			elif i == 1:
				name = picture_source_name1		
			elif i == 2:
				name = picture_source_name2		
			
			print name
			for j in range(3):
				openPicture(name)
				time.sleep(5)
				os.system('top -b -n 1 | grep eog | awk \'{print $11}\' >> ' + g_currentPath + picres +name +'.txt')
				os.system('killall eog')
				time.sleep(5)

		return

	elif kylin_version() == 'kylin 4.0':
		print ('this is kylin 4.0')
		name = ""
		for i in range(0, 3):
			if i == 0:
				name = picture_source_name
			elif i == 1:
				name = picture_source_name1
			elif i == 2:
				name = picture_source_name2	
	
			for j in range(3):			
				openPicture_kylin(name)
				time.sleep(3)
				os.system('top -b -n 1 | grep eom | awk \'{print $11}\' >> ' + g_currentPath + picres +name+'.txt')
				os.system('killall eom')
				time.sleep(3)	
			print name
				
		return
	
	elif g_osName == 'isoft':
		print ('this is isoft')

		name = ""
		for i in range(0, 3):
			if i == 0:
				name = picture_source_name	
			elif i == 1:
				name = picture_source_name1		
			elif i == 2:
				name = picture_source_name2		

				
			print name
			for j in range(3):
				openPicture_isoft(name)
				time.sleep(5)
				os.system('top -b -n 1 | grep gthumb | awk \'{print $11}\' >> ' + g_currentPath + picres +name+'.txt')
				os.system('killall gthumb')
				time.sleep(5)	
		
		return

if __main__=="__main__":
	main()
