#!/usr/bin/env python
#coding=utf-8

from ldtp 	import * 
from ldtputils 	import *
from time	import *
from os 	import *
from logging 	import *
from unittest   import *
import xml.dom.minidom
import commands
import sys

#sys.path.append(os.environ['AUTOTEST_PUBLIC_LIB'])
#publicIndex = g_currentPath.index('desktop')
#publicIndex += 7
#g_publicLibPath = sys.path[0][0:publicIndex] + '/public'
#sys.path.append(g_publicLibPath) 

g_publicLibPath = os.environ['AUTOTEST_PUBLIC_LIB']
sys.path.append(g_publicLibPath) 

from logcase import Logcase
#for XML parse
#******************************************
from caseobject import CaseObject
from ldtppub import LDTPPub
#******************************************
#an instance
mylog = Logcase()
#global screenshot  
Ldpub = LDTPPub()
#*****************************************   
g_tag = '1.3.1.1-ShowDDC'
g_currentPath = sys.path[0]
#*****************************************
global passwd
	
#************************************************************
#建立图像文件夹
def ckDir(dirName):
	try:
		if not os.path.exists(dirName):
			mylog.ilog(g_tag,'Beginning to create Pics Directory...' )
			if commands.getstatusoutput('mkdir ./resource')[0] == 0:
				os.system('mkdir ./result ./screenshot ')
				mylog.ilog(g_tag, 'Create ./resource successfully!')
			else:
				mylog.elog(g_tag, 'Create ./resource failed!')
				return False
		else:
			os.system('rm -rf ./screenshot/* ./result/*')
			mylog.ilog(g_tag,'Delete ./screenshot successfully!')
	except (NameError,Exception) as e:
		print e
	finally:
		return True

def setgrub():
	cmd = "echo " + passwd + " | sudo -S chmod a+w /boot/grub/grub.cfg >/dev/null"
	os.system(cmd)
	cmd = "echo " + passwd + " | sudo -S sed -i s/timeout=-1/timeout=1/g /boot/grub/grub.cfg >/dev/null"
	os.system(cmd)
	cmd = "echo " + passwd + " | sudo -S chmod a-w /boot/grub/grub.cfg >/dev/null"
	os.system(cmd)

def resetgrub():
	cmd = "echo " + passwd + " | sudo -S chmod a+w /boot/grub/grub.cfg >/dev/null"
	os.system(cmd)
	cmd = "echo " + passwd + " | sudo -S sed -i s/timeout=1/timeout=-1/g /boot/grub/grub.cfg > /dev/null"
	os.system(cmd)
	cmd = "echo " + passwd + " | sudo chmod a-w /boot/grub/grub.cfg >/dev/null"
	os.system(cmd)

#封装带有时间戳的抓屏幕窗口
#def Sceenshot(Win,Num):
#	if waittillguiexist(win) ==1:
#		imagecapture(Win,'/home/vans/.png')

#照片的名称用数字来表示
def imgCmp(num,ref):
	#判断参考文件是否存在
	if not os.path.exists(ref):
		mylog.elog(g_tag,'Referance file does not exists!')
		return False
	#申请对比照片的数量
	if num <= 0:
		mylog.elog(g_tag,'Invalid compaere items!')
		return False
	for i in range(num):
		res = imagecompare('./screenshot/%s' % num, ref)
		if res >= 2:
			mylog.elog(g_tag,'./screenshot/%s' % num )
			return False
		num -=1
		#0不需要做对比
		if num == 0:
			break
	mylog.ilog(g_tag,'I am return from imgCmp...')
	return True
	
	
			
#打开DDC显示窗口
def cosfrmDisplay(Num):
	##os.system('/usr/bin/python /usr/lib/cinnamon-settings/cinnamon-settings.py &')
	#Ldpub.setResolution('cos', '1920', '1080'
	##activatewindow(u'frm系统设置面板')
	
	##controlFrame = u'frm系统设置面板'
        ##setObjList = getobjectlist(controlFrame)
	##commonStr = u'cbo常用设置' # change to unicode to compare
		
        ##if commonStr in setObjList: 
	  ##  print 'cbo common settings'
	    ##if mouseleftclick('系统设置面板', '修改屏幕分辨率') == 1:
		##mylog.ilog(g_tag, 'Open display resolution setting panel ok')
		
	##else:
	  ##  print 'cbo all settings'
            ##if mouseleftclick('系统设置面板', 'ico27') == 1:
              ##      mylog.ilog(g_tag, 'Open display resolution setting panel ok')
                    
	print '*******************************************'	
	os.system('cinnamon-settings display &')
	sleep(5)
	if waittillguiexist(u'frm\u7cfb\u7edf\u8bbe\u7f6e\u9762\u677f') ==1:
		print 'I catch the Window...'	
		imagecapture(u'frm\u7cfb\u7edf\u8bbe\u7f6e\u9762\u677f','./screenshot/%s' % Num)
		sleep(5)
		#activateindow(u'frm\u7cfb\u7edf\u8bbe\u7f6e\u9762\u677f')
		#if guiexist(u'frm\u7cfb\u7edf\u8bbe\u7f6e\u9762\u677f') ==1:	
		#关闭窗口
		print 'I will close the window.........'
		mylog.ilog(g_tag,'I close the Window!')
		keypress('<alt>')
		keypress('<F4>')
		keyrelease('<alt>')
		keyrelease('<F4>')
		sleep(5)
		return True
	else:
		print 'I cann\'t find window: frm 系统设置面板'
		return False
	 
	closewindow(u'frm\u7cfb\u7edf\u8bbe\u7f6e\u9762\u677f')
	return True

#打开DDC显示窗口
def isoftfrmDisplay(Num):
	#os.system('/usr/bin/python /usr/lib/cinnamon-settings/cinnamon-settings.py &')
	#print 'The current window list is :', getwindowlist()
	#activatewindow(u'frm\u7cfb\u7edf\u8bbe\u7f6e')	
	os.system('cinnamon-settings display &')
	sleep(5)
	#Ldpub.setResolution('isoft', '1920', '1080')
	if waittillguiexist(u'frm\u7cfb\u7edf\u8bbe\u7f6e') ==1:
		print 'I catch the window.......'
		#scrolldown(u'frm\u7cfb\u7edf\u8bbe\u7f6e','scbr1')
		#sleep(2)
		#mouseleftclick(u'frm\u7cfb\u7edf\u8bbe\u7f6e','ico32')
		#sleep(2)
		print '*******************************************'
		imagecapture(u'frm\u7cfb\u7edf\u8bbe\u7f6e', './screenshot/%s' % Num)
		sleep(5)

		print 'I will close the window.........'
		keypress('<alt>')
		keypress('<F4>')
		keyrelease('<alt>')
		keyrelease('<F4>')
		sleep(5)
		return True
	
	closewindow(u'frm\u7cfb\u7edf\u8bbe\u7f6e\u9762\u677f')
	return True

#专门执行S3/S4的操作
def powerControl(Sd):
	global passwd
	if Sd == 3:
		if os.environ['S3_ENABLE'] =='1':
			res = commands.getstatusoutput('echo %s | sudo -S rtcwake -m mem -s 120' % passwd)[0]
		else:
			print 'S3 OP is canceled!'
			mylog.wlog(g_tag,'S3 OP is canceled!')
			res = '1'
			
			if res != 0:
				#print 'S3 excute failed!'
				#mylog.elog(g_tag,'S3 excute failed!')
				return False
			

			
	elif Sd == 4:
		if os.environ['S4_ENABLE'] =='1':
			res = commands.getstatusoutput('echo %s | sudo -S rtcwake -m disk -s 120' % passwd)[0]
		else:
			print 'S4 OP is canceled!'
			mylog.wlog(g_tag,'S4 OP is canceled!')
			res = '1'
		if res != 0:
			#print 'S4 excute failed!'
			#mylog.elog(g_tag,'S4 excute failed!')
			return False
	else:
		#print 'Invalid State'
		mylog.elog(g_tag,'Invalid State!')
	return True


def isoft_Work():
	num = range(10)
	rest = isoftfrmDisplay(num[0])
	for i in range(1):
		if rest == True:
			sleep(3)
			powerControl(3)
			sleep(10)
			isoftfrmDisplay(num[i+1])
			sleep(3)
			powerControl(4)
			sleep(10)
			isoftfrmDisplay(num[i+2])
		else:
			break

	res = imgCmp(2, './screenshot/0')
	if res != True:
		mylog.elog(g_tag, 'Exist The result you don\'t want!')
	else:
		print 'Well Done!'
		mylog.ilog(g_tag, 'Well Done vans, Come On!')
	return 
	

def cos_Work():
	num = range(10)
	rest = cosfrmDisplay(num[0])
	for i in range(1):
		if rest == True:
			sleep(3)
			powerControl(3)
			sleep(10)
			cosfrmDisplay(num[i+1])
			sleep(3)
			powerControl(4)
			sleep(10)
			cosfrmDisplay(num[i+2])
		else:
			break

	res = imgCmp(2, './screenshot/0')
	if res != True:
		mylog.elog(g_tag, 'Exist The result you don\'t want!')
	else:
		print 'Well Done!'
		mylog.ilog(g_tag, 'Well Done vans, Come On!')
	return 
	

def kylin_Work():
	#create result log
	cmd0 = 'xrandr -q | grep \connected >>'
	cmd1 = 'xrandr -q | grep \* >>'
	cmd2 = 'xrandr -q | grep \Screen >>'

	os.system('touch ./result/DDC_NoramlInfo')
	os.system('touch ./result/DDC_AfterS3Info')
	os.system('touch ./result/DDC_AfterS4Info')
	print 'Normal DDC informaion!'
	os.system(cmd0+'./result/DDC_NoramlInfo')
	os.system(cmd1+'./result/DDC_NoramlInfo')
	os.system(cmd2+'./result/DDC_NoramlInfo')
	sleep(3)
	powerControl(3)
	sleep(10)
	os.system(cmd0+'./result/DDC_AfterS3Info')
	os.system(cmd1+'./result/DDC_AfterS3Info')	
	os.system(cmd2+'./result/DDC_AfterS3Info')
	sleep(3)
	powerControl(4)
	sleep(10)
	os.system(cmd0+'./result/DDC_AfterS4Info')
	os.system(cmd1+'./result/DDC_AfterS4Info')
	os.system(cmd2+'./result/DDC_AfterS4Info')
	
	res0 = commands.getstatusoutput('diff ./result/DDC_NoramlInfo ./result/DDC_AfterS3Info')[1] == ''
	res1 = commands.getstatusoutput('diff ./result/DDC_NoramlInfo ./result/DDC_AfterS4Info')[1] == ''
	if res0 != True:
		print 'After S3 DDC information has changed!'
	elif res1 != True:
		print 'After S4 DDC information has changed!'
	else:
		print 'DDC information is not changed!'
	return True
		 



def main():
	global passwd
	obj = CaseObject(g_tag, g_currentPath + '/' + g_tag + '.xml')
	#调用getOSName 方法 脚本执行环境判断
	os_type = obj.getOSName()
	passwd = obj.getPasswd()
	num = range(10)
	Path = os.path.abspath(os.path.dirname(sys.argv[0]))
	chdir(Path)
	res = ckDir('./resource')
	if res != True:
		print 'Directory struct is not complement!'	
		return
	#总体循环次数
	#获取参考文件
	if cmp(os_type, 'cos') ==0:
		setgrub()
		cos_Work()
	elif cmp(os_type, 'isoft') ==0:
		setgrub()
		isoft_Work()
	else:
		kylin_Work()
		return
		
	sleep(2)
	os.system('mv ./screenshot/0  ./screenshot/ShowDDC_Normal')
	os.system('mv ./screenshot/1  ./screenshot/ShowDDC_AfterS3')
	os.system('mv ./screenshot/2  ./screenshot/ShowDDC_AfterS4')
	sleep(5)

	if ((cmp(os_type, 'cos') ==0) or (cmp(os_type, 'isoft') ==0)):
			resetgrub()
	sleep(5)
	return True

if __name__ == '__main__':
	main()


