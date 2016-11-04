#!/usr/bin/env python
#coding=utf-8
#########################################################################
# 1.2.2-verinfo.py
# Date: 2015/5/7
# Test Version: MICFangde_V1.0_20150401
# Property: Case
# Function: Output the version information into files
#########################################################################

import os
import sys
import time
import shutil

sys.path.append(os.environ['AUTOTEST_PUBLIC_LIB'])

from caseobject import CaseObject
from logcase import Logcase

g_currentPath = sys.path[0]
g_tag = '1.2.2-verinfo'
g_log = Logcase()
g_outputDir = None
g_outputKernelVersionFile = None
g_outputSysVersionFile = None
g_os = None

def execCommand(command, comment):
    if os.system(command) != 0:
        logStr = ': error exec ' + command + ' for ' + comment
        totalLogStr = g_tag + logStr
        print totalLogStr
        g_log.elog(g_tag, logStr)
        return False
    else:
        logStr = ': success exec ' + command + ' for ' + comment
        totalLogStr = g_tag + logStr
        print totalLogStr
        g_log.ilog(g_tag, logStr)
        return True

def checkKernelVersion():
    if g_outputKernelVersionFile != None:
        cmd =  'uname -r >' + g_outputKernelVersionFile
        execCommand(cmd, 'getting kernel version')

def checkSystemVersion():
    if g_outputSysVersionFile == None or g_os == None:
        return
  
    sysInfoFile = '/etc/os-release'
    if g_os == 'isoft':
        sysInfoFile = '/etc/version' 
    
    if not os.path.exists(sysInfoFile):
        os.system('touch %s/因系统文件不存在无法读系统信息' %(g_outputDir))
        g_log.wlog(g_tag, 'File %s not exists, please check system again' % sysInfoFile)
	return 
    # kylin system info file: .product_info / .productinfo
    if g_os == 'kylin':
        sysInfoFile = '/etc/.product_info'
        print 'TEST: in test %s' %sysInfoFile
	if not os.path.exists(sysInfoFile):
            sysInfoFile = '/etc/.productinfo'
            if not os.path.exists(sysInfoFile):
                print 'TEST: in test %s' %sysInfoFile
	        os.system('touch %s/因系统文件不存在无法读系统信息' %(g_outputDir))
	        g_log.wlog(g_tag, 'File %s not exists, please check system again' % sysInfoFile)
	        return 

    cmd = 'cat ' + sysInfoFile + ' > ' + g_outputSysVersionFile
    execCommand(cmd, 'getting system version')

def initArguments():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    global g_outputDir
    global g_outsideProgramPath
    global g_os
    global g_outputSysVersionFile
    global g_outputKernelVersionFile
    global g_outputDir

    obj = CaseObject(g_tag, g_currentPath + '/' + g_tag + '.xml')
    
    doc = obj.getDocumentNode()
    dataNode = obj.getXMLNode(doc,'data', 0)
    outputFileNode = obj.getXMLNode(dataNode,'system_version_ouput', 0)
    if outputFileNode != None:
        g_outputSysVersionFile = g_currentPath + '/' + obj.getXMLNodeValue(outputFileNode, 0)
    else:
        g_log.elog(g_tag, 'XML config: output_dir node set incorrect')
        return False

    outputFileNode = obj.getXMLNode(dataNode,'kernel_version_ouput', 0)
    if outputFileNode != None:
        g_outputKernelVersionFile = g_currentPath + '/' + obj.getXMLNodeValue(outputFileNode, 0)
    else:
        g_log.elog(g_tag, 'XML config: output_dir node set incorrect')
        return False

    g_outputDir = g_currentPath + '/' + os.path.dirname(obj.getXMLNodeValue(outputFileNode, 0))

    try:
	if os.path.exists(g_outputDir):
            if os.path.isfile(g_outputDir):
                g_log.ilog(g_tag, 'A rename output file exists, Create a new folder to save output file' + g_outputDir)
                os.remove(g_outputDir)
	    else:
                shutil.rmtree(g_outputDir)
 
        os.makedirs(g_outputDir) # create result directory anyhow
    except: 
        g_log.elog(g_tag, 'Cannot save output files in' + g_outputDir)
        return False

    g_os = obj.getOSName()
    return True

def main():
    if initArguments():
        checkKernelVersion()
        checkSystemVersion()
    
if __name__ == '__main__':
    main()
