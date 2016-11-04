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

g_currentPath = sys.path[0]
sys.path.append(os.environ['AUTOTEST_PUBLIC_LIB'])
g_s4 = int(os.environ['S4_ENABLE'])
print "s4 enable is "
print g_s4
#timeStamp = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
timeStamp = ''

if not os.path.exists(g_currentPath + '/resource'):
    os.system('mkdir -p '+ g_currentPath + '/resource')

pcusername=getpass.getuser()

from logcase import Logcase
from caseobject import CaseObject
g_log = Logcase()

picobj = CaseObject('1.8.1.1-kmusbvalue',g_currentPath + '/1.8.1.1-kmusbvalue.xml')
doc = picobj.getDocumentNode()
g_osName = picobj.getOSName()

from screenshot import Screenshot
g_sst = Screenshot()

common_node = picobj.getXMLNode(doc,'common',0)
count_node = picobj.getXMLNode(common_node, 'count', 0)
count = picobj.getXMLNodeValue(count_node, 0)
print (count)

data_node = picobj.getXMLNode(doc,'data',0)

password = picobj.getPasswd()
print (password)

g_mode = ''

def wakeup_mode():
        global g_mode
        if g_mode == 's3':
		os.system('echo '+password+' | sudo -S rtcwake -m mem -s 90')
                time.sleep(10)
        if g_mode == 's4' and g_s4 == 1:
		os.system('echo '+password+' | sudo -S rtcwake -m disk -s 120') 
                time.sleep(10)
        return

def open_file_cos():
        global timeStamp
	count = 0
	timeStamp = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
	time.sleep(2)
        print ('is opening file ')
	while(count < 3):
		os.system('gedit '+ g_currentPath + '/result/'+timeStamp+'key_mouse.txt &')
		time.sleep(2)
		if guiexist('*-Gedit编辑器') == 0:
			count += 1
			continue
		else:
			break
               
	print ('open file finish ')
	return

def open_file_lylin():
	g_log.ilog('keymouse_log','is opening file')
        global timeStamp
	count = 0
	timeStamp = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
	time.sleep(2)
        print ('is opening file ')
	while(count < 3):
		os.system('gedit '+ g_currentPath + '/result/'+timeStamp+'key_mouse.txt &')
		time.sleep(2)
		if guiexist('*-记事本') == 0:
			count += 1
			continue
		else:
			break
               
	print ('open file finish ')
	return

def open_file_isoft():
	g_log.ilog('keymouse_log','is opening file')
        global timeStamp
	count = 0
	timeStamp = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
	time.sleep(2)
        print ('is opening file ')
	while(count < 3):
		os.system('gedit '+ g_currentPath + '/resource/'+timeStamp+'key_mouse.txt &')
		time.sleep(2)
		if guiexist('*-gedit') == 0:
			count += 1
			continue
		else:
			break
               
	print ('open file finish ')
	return

def write_file():
	global g_mode
	print g_currentPath+'/resource/cnee'
	print g_currentPath+'/resource/xne.xns'
	time.sleep(3)
	os.system(g_currentPath+'/resource/cnee -rep -f '+g_currentPath+'/resource/xnee.xns')
	print 'xnee end .....'
	time.sleep(5)	
	g_mode = 's3'
	wakeup_mode()
	g_mode = 's4'
	wakeup_mode()
	keypress('<alt>')
	keypress('<F4>')
	keyrelease('<alt>')
	keyrelease('<F4>')
	time.sleep(3)


	#os.system('vi '+ g_currentPath + '/resource/'+timeStamp+'key_mouse.txt')
	#time.sleep(3)
	#keypress('<alt>')
	#keypress('<F4>')
	#keyrelease('<alt>')
	#keyrelease('<F4>')
	#time.sleep(3)
	#keypress('<alt>')
	#keypress('l')
	#keyrelease('<alt>')
	#keyrelease('l')
	return			

def write_file_kylin():
	g_log.ilog('keymouse_log','is writing file')
	global g_mode
	global g_mode
	print g_currentPath+'/resource/cnee-64'
	print g_currentPath+'/resource/xne.xns'
	time.sleep(3)
	os.system(g_currentPath+'/resource/cnee-64 -rep -f '+g_currentPath+'/resource/xnee_kylin_64.xns')
	print 'xnee end .....'
	time.sleep(5)	
	g_mode = 's3'
	wakeup_mode()
	g_mode = 's4'
	wakeup_mode()
	keypress('<alt>')
	keypress('<F4>')
	keyrelease('<alt>')
	keyrelease('<F4>')
	time.sleep(3)


	return

def write_file_isoft():
	g_log.ilog('keymouse_log','is writing file')
	global g_mode
	print g_currentPath+'/resource/cnee'
	print g_currentPath+'/resource/xne_isoft.xns'
	time.sleep(3)
	os.system(g_currentPath+'/resource/cnee -rep -f '+g_currentPath+'/resource/0611_isoft.xns')
	print 'xnee end .....'
	time.sleep(5)	
	g_mode = 's3'
	wakeup_mode()
	g_mode = 's4'
	wakeup_mode()
	keypress('<alt>')
	keypress('<F4>')
	keyrelease('<alt>')
	keyrelease('<F4>')
	time.sleep(3)

	return	

def main(): 
	print ('starting key mouse')
	print g_osName
	if g_osName == 'cos':
		open_file_cos()
		time.sleep(2)
		write_file()
        	return

	if g_osName == 'kylin':
		print('this is kylin')
		open_file_lylin()
		time.sleep(2)
		write_file_kylin()
		return

	if g_osName == 'isoft':
		print('this is isoft')
		open_file_isoft()
		time.sleep(2)
		write_file_isoft()
		return

if __main__=="__main__":
    main()




