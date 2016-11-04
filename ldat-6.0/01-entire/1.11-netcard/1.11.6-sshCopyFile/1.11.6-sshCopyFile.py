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
resourcedir = '/resource/'

os.system('rm -rf '+ g_currentPath + '/result/*')

sys.path.append(os.environ['AUTOTEST_PUBLIC_LIB'])

from logcase import Logcase
from caseobject import CaseObject

path = CaseObject('1.11.6-sshCopyFile',g_currentPath + '/1.11.6-sshCopyFile.xml')
doc = path.getDocumentNode()

data_node = path.getXMLNode(doc,'data',0)
source = path.getXMLNode(data_node, 'source_path', 0)
source_path = path.getXMLNodeValue(source, 0)

destination = path.getXMLNode(data_node, 'destination_path', 0)
destination_path = path.getXMLNodeValue(destination, 0)
destination_path = g_currentPath + destination_path

host_passward = path.getXMLNode(data_node, 'another_host_passward', 0)
another_host_passward = path.getXMLNodeValue(host_passward, 0)

expect = g_currentPath + resourcedir + 'expect.deb'

password = path.getPasswd()

def main():
	print ' >>source_path is ' + source_path
	print ' >>destination_path is ' + destination_path
	print ' >>another_host_passward is ' + another_host_passward
	
	for i in range(0, 3):
		os.system(g_currentPath + resourcedir + 'sshCopyFile.sh' + ' ' + source_path + ' ' +
	      	destination_path + ' ' + another_host_passward + ' ' + expect + ' ' + password)
		string = os.listdir(destination_path)
		err = len(string)
		if err == 1:
			print ' >> scp success'
			break
		else:
			print ' >> scp failure'
	
if __main__=="__main__":
	main()
