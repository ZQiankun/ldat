#!/usr/bin/env python
#coding=utf-8

#########################################################################
# system_info.py
# Date: 2015/4/23
# Test Version: MICFangde_V1.0_20150401
# Property: Case
# Function: Output the system information(etc., cpu, harddisk) into files.
#########################################################################

import os
import sys
import time
import commands
import shutil

#temp1="/home/lenovo/work/ldat/189-svn-ldat/ldat/public"
sys.path.append(os.environ['AUTOTEST_PUBLIC_LIB'])
#sys.path.append(temp1)

from caseobject import CaseObject
from logcase import Logcase

g_currentPath = sys.path[0]
g_tag = '1.2.5-1.2.11-sysinfo'
g_log = Logcase()
g_outputDir = None
g_outsideProgramPath = None
g_passwd = None
g_osBit = None

def enableDir(fileTotalPath):
    dirPath = os.path.dirname(fileTotalPath)
    print 'dirPath %s' %dirPath

    command = 'echo ' + '\'' + g_passwd + '\'|'+ 'sudo -S ' + 'chmod -R a+x ' + dirPath
    if os.system(command) != 0:
        print 'Error enable dir %s' %dirPath
        return False

    return True

def initArguments():
    global g_outputDir
    global g_outsideProgramPath
    global g_passwd
    global g_osBit

    obj = CaseObject(g_tag, g_currentPath + '/' + g_tag + '.xml')

    g_passwd = obj.getPasswd()
    g_osBit = obj.identifyOSBit()
    if g_passwd == None:
        g_log.elog(g_tag, 'Cannot execute program for root')
        return False
    
    doc = obj.getDocumentNode()
    dataNode = obj.getXMLNode(doc,'data', 0)
    outputDirNode = obj.getXMLNode(dataNode,'output_dir', 0)
    if outputDirNode != None:
        g_outputDir = g_currentPath + '/' + obj.getXMLNodeValue(outputDirNode, 0)
    else:
        g_log.elog(g_tag, 'XML config: output_dir node set incorrect')
        return False

    """
    outsideNode = obj.getXMLNode(dataNode,'outside_program',0)
    if outsideNode != None:
        g_outsideProgramPath = g_currentPath + '/' + obj.getXMLNodeValue(outsideNode, 0)
    else:
        g_log.elog(g_tag, 'XML config: outside_program set incorrect')
        return False

    if not enableDir(g_outsideProgramPath):
        return False

    print 'output_dir %s, g_outsideProgramPath %s' %(g_outputDir, g_outsideProgramPath)
    """

    try:
	if os.path.exists(g_outputDir):
            if os.path.isfile(g_outputDir):
		print '1.2.5: remove file'
                os.remove(g_outputDir)
            else:
		print '1.2.5: remove dir'
                shutil.rmtree(g_outputDir)
        os.makedirs(g_outputDir)
    except: 
        g_log.elog(g_tag, 'Cannot save output files in' + g_outputDir)
        return False

    return True

def installTools(osBit, pkgType, toolName, pkgPath):
	try:
		ret = os.system('which ' + toolName)
		if ret == 0:
#		ret, out = commands.getstatusoutput('which ' + toolName)
#		if len(out) > 0 and out.find('no') == -1:
			print '%s has been installed' %toolName
			return True
		
		command = ''
		if osBit == '32' and pkgType == 'deb':
			ret = os.system('which dpkg')
#			ret1, out1 = commands.getstatusoutput('which dpkg')	
			if ret == 0:
#			if len(out1) > 0:
				print 'install ethtool deb for 32 bit os'
				command = 'echo ' + g_passwd + '| sudo -S dpkg -i ' + g_currentPath + '/resource' + pkgPath 
			else:	
				logStr = 'has no dpkg tool'
				return False
		elif osBit == '64' and pkgType == 'rpm':
			ret = os.system('which rpm')
			if ret == 0:
#			ret1, out1 = commands.getstatusoutput('which rpm')	
#			if len(out1) > 0:
				print 'install ethtool rpm for 64 bit os'
				command = 'echo ' + g_passwd + '| sudo -S rpm -i ' + g_currentPath + '/resource' + pkgPath
			else:	
				logStr = 'has no rpm tool'
				return False
		else:
			logStr = 'in' + g_osBit + ' bit os with ' + pkgType + ', has no ethtool package to install'
			print logStr 
			g_log.wlog(g_tag, logStr)
		os.system(command) # install package
		return True
	except:
		logStr = 'find ' + toolName + ' package to install error'
		print logStr 
		g_log.wlog(g_tag, logStr)
		return False

def runVisualOutput():
    rootPath = os.environ['AUTOTEST_DIR'] + '/'
    try:
	if g_osBit == '32':
		installTools(g_osBit, 'deb', 'ethtool', '/deb32/ethtool_3.1-1_i386.deb')
		installTools(g_osBit, 'deb', 'hdparm', '/deb32/hdparm_9.37-0ubuntu3_i386.deb')
		command = 'echo ' + g_passwd + '| sudo -S bash '+ g_currentPath + '/resource/1.2.5-1.2.11-runprogram.sh '+ g_currentPath + '/resource/program32/SystemInfo32' + ' ' + g_outputDir + ' ' + rootPath + 'tools/visualcfg'
	elif g_osBit == '64':
		installTools(g_osBit, 'rpm', 'ethtool', '/rpm64/ethtool-3.8-1.nk.1.x86_64.rpm')
		installTools(g_osBit, 'rpm', 'hdparm', '/rpm64/hdparm-9.42-2.nk.1.x86_64.rpm')
		command = 'echo ' + g_passwd + '| sudo -S bash '+ g_currentPath + '/resource/1.2.5-1.2.11-runprogram.sh '+ g_currentPath + '/resource/program64/SystemInfo64' + ' ' + g_outputDir + ' ' + rootPath + 'tools/visualcfg64'
		# Add code special for V3
		if os.system('cat /etc/issue | head -1 | grep "NeoKylin 3"') == 0:
			command = 'echo ' + g_passwd + '| sudo -S bash '+ g_currentPath + '/resource/1.2.5-1.2.11-runprogram.sh '+ g_currentPath + '/resource/programV3/SystemInfo64' + ' ' + g_outputDir + ' ' + rootPath + 'tools/visualcfgV3'

        if os.system(command) != 0:
            logStr = 'execute ' + command + ' error, please check if the file exists.'
            g_log.elog(g_tag, logStr)
            return False

        logStr = 'execute ' + command + ' ok, please open folder' + g_outputDir + 'to check the output system information files.'
        g_log.ilog(g_tag, logStr)
       
#        time.sleep(60) # wait the program end
        return True
    except:
        g_log.elog(g_tag, 'Cannot execute program for root')


def main():
    if initArguments():        
        runVisualOutput()
    
if __name__ == '__main__':
    main()
