#!/usr/bin/env python
#coding=utf-8
#########################################################################
# 1.2.1-synctime.py
# Date: 2015/6/5
# Test Version: MICFangde_V1.0_20150401
# Property: Case
# Function: Check if the system time is synchronized with BIOS time
#########################################################################

import os
import sys
import re
from commands import getstatusoutput
from re import match

#sys.path.append('/home/luzh/work/132-svn/ldat/public')
sys.path.append(os.environ['AUTOTEST_PUBLIC_LIB'])

from caseobject import CaseObject
from logcase import Logcase

g_currentPath = sys.path[0]
g_tag = '1.2.1-synctime'
g_log = Logcase()
g_passwd = None

g_resultFile = g_currentPath + '/result/result.txt'
g_resultFolder = g_currentPath + '/result'

def execCommand(command, comment):
    ret, out = getstatusoutput(command)
    if os.system(command) != 0:
        logStr = ': error exec ' + command + ' for ' + comment
        totalLogStr = g_tag + logStr
        print totalLogStr
        g_log.elog(g_tag, logStr)
        return False, out
    else:
        logStr = ': success exec ' + command + ' for ' + comment
        totalLogStr = g_tag + logStr
        print totalLogStr
        g_log.ilog(g_tag, logStr)
        return True, out

def compareTime(osTimeResult, biosTimeResult):
    matchStr = '.*(\d{4}年\d+月\d+日).*(\d{2}时\d+分\d+秒).*'
    groupNum = 2
    osTimeMatch = match(matchStr, osTimeResult)
    biosTimeMatch = match(matchStr, osTimeResult)

    try:
        for i in range(groupNum):
            if osTimeMatch.group(i) != biosTimeMatch.group(i):
                logStr = 'os time is not synchronized bios time, os time is %s, but bios time is %s' % (osTimeResult, biosTimeResult)
                print logStr
                g_log.elog(g_tag, logStr)
                return False

        logStr = 'os time is synchronized bios time, os time is %s, and bios time is %s' % (osTimeResult, biosTimeResult)
        print logStr
        g_log.ilog(g_tag, logStr)
        return True

    except:
        logStr = 'match time str error, os time is %s, and bios time is %s' % (osTimeResult, biosTimeResult)
        print logStr
        g_log.elog(g_tag, logStr)
        return False

def initArguments():
    global g_passwd
    obj = CaseObject(g_tag, g_currentPath + '/' + g_tag + '.xml')
    g_passwd = obj.getPasswd()
    print 'passwd is ', g_passwd

    if g_passwd == None:
        return False
    else:
        return True

def createResultFolder():
    if not os.path.exists(g_resultFolder) or not os.path.isdir(g_resultFolder):
        os.makedirs(g_resultFolder)

def getTime():
    # ret, osTimeResult = execCommand('date -d today +"%Y年%m月%d日 %H时%M分%S秒"', 'get os time')
    # ret, osTimeResult = execCommand('date | tee -a %s' %(g_resultFile), 'get os time')
    ret, osTimeResult = execCommand('date', 'get os time')
    if not ret:
        return None, None
    print 'osTimeResult', osTimeResult

    ret, biosTimeResult = execCommand('echo %s | sudo -S hwclock --localtime' %(g_passwd), 'get bios time')
    matchStr = match('(.*:)(.*)', biosTimeResult)
    try:
	biosTimeResult = matchStr.group(2)
    except:
	pass

    if not ret:
        return None, None

    return osTimeResult, biosTimeResult

def main():
    if not initArguments():
        return

    createResultFolder()
    osTimeResult, biosTimeResult = getTime()
    logStr = 'Os time is %s,BIOS time is %s' % (osTimeResult, biosTimeResult)

    logList = logStr.split(',')
    with open(g_resultFile, 'w') as fp:
	for s in logList:
	   fp.write(s)
	   fp.write('\n')

    print logStr
    g_log.ilog(g_tag, logStr)
    
if __name__ == '__main__':
    main()
