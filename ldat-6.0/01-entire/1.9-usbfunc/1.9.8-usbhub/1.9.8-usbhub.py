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
print g_currentPath

usbdir = '/resource/'

if not os.path.exists(g_currentPath + usbdir):
    os.system('mkdir -p '+ g_currentPath + usbdir)

pcusername=getpass.getuser()

sys.path.append(os.environ['AUTOTEST_PUBLIC_LIB'])

from logcase import Logcase
from caseobject import CaseObject
g_log = Logcase()

picobj = CaseObject('1.9.8-usbhub',g_currentPath + '/1.9.8-usbhub.xml')
doc = picobj.getDocumentNode()
g_osName = picobj.getOSName()

from screenshot import Screenshot
g_sst = Screenshot()

common_node = picobj.getXMLNode(doc,'common',0)
count_node = picobj.getXMLNode(common_node, 'count', 0)
count = picobj.getXMLNodeValue(count_node, 0)
print (count)

data_node = picobj.getXMLNode(doc,'data',0)



usb_resource = picobj.getXMLNode(data_node, 'resource_name', 0)
usb_resource_name = picobj.getXMLNodeValue(usb_resource, 0)
print (usb_resource_name)
usb_dev_name = picobj.getXMLNode(data_node, 'usb_device_name', 0)
usb_device_name = picobj.getXMLNodeValue(usb_dev_name, 0)
print (usb_device_name)


usb_resource1 = picobj.getXMLNode(data_node, 'resource_name1', 0)
usb_resource_name1 = picobj.getXMLNodeValue(usb_resource1, 0)
print (usb_resource_name1)
usb_dev_name1 = picobj.getXMLNode(data_node, 'usb_device_name1', 0)
usb_device_name1 = picobj.getXMLNodeValue(usb_dev_name1, 0)
print (usb_device_name1)


usb_resource2 = picobj.getXMLNode(data_node, 'resource_name2', 0)
usb_resource_name2 = picobj.getXMLNodeValue(usb_resource2, 0)
print (usb_resource_name2)
usb_dev_name2 = picobj.getXMLNode(data_node, 'usb_device_name2', 0)
usb_device_name2 = picobj.getXMLNodeValue(usb_dev_name2, 0)
print (usb_device_name2)


usb_resource3 = picobj.getXMLNode(data_node, 'resource_name3', 0)
usb_resource_name3 = picobj.getXMLNodeValue(usb_resource3, 0)
print (usb_resource_name3)
usb_dev_name3 = picobj.getXMLNode(data_node, 'usb_device_name3', 0)
usb_device_name3 = picobj.getXMLNodeValue(usb_dev_name3, 0)
print (usb_device_name3)


password = picobj.getPasswd()
print (password)


def read_and_write_cos(usbname,resourcename):
	if not os.path.exists('/media/'+pcusername+'/'+usbname+'/'+resourcename):
            	g_log.elog('usb_log','USB device not resource')
	        print('usb device not resource ')
		return 
	os.system('cp /media/'+pcusername+'/'+usbname+'/'+resourcename+' '+g_currentPath + '/resource/')
	time.sleep(2)
	
	while 1:
		if os.path.exists(g_currentPath+ '/resource/' +resourcename):
			break
	time.sleep(5)
	print ('diff '+g_currentPath +'/resource/' + resourcename+ ' /media/'+pcusername+'/'+usbname+'/'+resourcename)
	if os.system('diff '+g_currentPath + '/resource/'+resourcename+ ' /media/'+pcusername+'/'+usbname+'/'+resourcename) == 0:
		print ('USB device read success')
		g_log.ilog('usb_log','USB device read success')

	os.system('rm -rf /media/'+pcusername+'/'+usbname+'/'+resourcename)
	os.system('cp '+g_currentPath+'/resource/'+resourcename+' /media/'+pcusername+'/'+usbname)
	while 1:
		if os.path.exists('/media/'+pcusername+'/'+usbname+'/'+resourcename):
			break
	time.sleep(5)
	if os.system('diff '+g_currentPath + '/resource/'+resourcename+ ' /media/'+pcusername+'/'+usbname+'/'+resourcename) == 0:
		print ('USB device write success')
		g_log.ilog('usb_log','USB device write success')

	os.system('rm '+g_currentPath+'/resource/'+resourcename)
	return

def read_and_write_kylin(usbname,resourcename):
	if not os.path.exists('/run/media/'+pcusername+'/'+usbname+'/'+resourcename):
            	g_log.elog('usb_log','USB device not resource')
	        print('usb device not resource ')
		return 
	os.system('cp /run/media/'+pcusername+'/'+usbname+'/'+resourcename+' '+g_currentPath + '/resource/')
	time.sleep(2)
	
	while 1:
		if os.path.exists(g_currentPath+ '/resource/' +resourcename):
			break
	time.sleep(5)
	print ('diff '+g_currentPath +'/resource/' + resourcename+ ' /run/media/'+pcusername+'/'+usbname+'/'+resourcename)
	if os.system('diff '+g_currentPath + '/resource/'+resourcename+ ' /run/media/'+pcusername+'/'+usbname+'/'+resourcename) == 0:
		print ('USB device read success')
		g_log.ilog('usb_log','USB device read success')

	os.system('rm -rf /run/media/'+pcusername+'/'+usbname+'/'+resourcename)
	os.system('cp '+g_currentPath+'/resource/'+resourcename+' /run/media/'+pcusername+'/'+usbname)
	while 1:
		if os.path.exists('/run/media/'+pcusername+'/'+usbname+'/'+resourcename):
			break
	time.sleep(5)
	if os.system('diff '+g_currentPath + '/resource/'+resourcename+ ' /run/media/'+pcusername+'/'+usbname+'/'+resourcename) == 0:
		print ('USB device write success')
		g_log.ilog('usb_log','USB device write success')

	os.system('rm '+g_currentPath+'/resource/'+resourcename)
	return

def main():
	if g_osName == 'cos' or g_osName == 'isoft':
	    usbname = ''
	    resourcename = ''
	    for i in range(0, 4):
		if i == 0:
	        	usbname = usb_device_name
	        	resourcename = usb_resource_name
	
		elif i == 1:
	        	usbname = usb_device_name1
	        	resourcename = usb_resource_name1			
		elif i == 2:
	        	usbname = usb_device_name2
	        	resourcename = usb_resource_name2		
		elif i == 3:
	        	usbname = usb_device_name3
	        	resourcename = usb_resource_name3

                read_and_write_cos(usbname,resourcename)
            return

	if g_osName == 'kylin':
	    print ('this is kylin')
	    usbname = ''
	    resourcename = ''	
	    for i in range(0, 4):
		if i == 0:
	        	usbname = usb_device_name
	        	resourcename = usb_resource_name
	
		elif i == 1:
	        	usbname = usb_device_name1
	        	resourcename = usb_resource_name1			
		elif i == 2:
	        	usbname = usb_device_name2
	        	resourcename = usb_resource_name2		
		elif i == 3:
	        	usbname = usb_device_name3
	        	resourcename = usb_resource_name3
            	read_and_write_kylin(usbname,resourcename)

            return

if __main__=="__main__":
    main()




