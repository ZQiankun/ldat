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
import codecs 
import subprocess

g_currentPath = sys.path[0]
sys.path.append(os.environ['AUTOTEST_PUBLIC_LIB'])


picdir = '/result/'

if not os.path.exists(g_currentPath + picdir):
	os.system('mkdir -p '+ g_currentPath + picdir)

if os.path.exists(g_currentPath + picdir+'appVersions.txt'):
	os.system('rm -rf '+ g_currentPath + picdir+'appVersions.txt')

from logcase import Logcase
from caseobject import CaseObject
g_log = Logcase()

#parse xml
picobj = CaseObject('1.2.12-CheckAppVersionInfo',g_currentPath + '/1.2.12-CheckAppVersionInfo.xml')
doc = picobj.getDocumentNode()

common_node = picobj.getXMLNode(doc,'common',0)
count_node = picobj.getXMLNode(common_node, 'count', 0)
count = picobj.getXMLNodeValue(count_node, 0)

data_node = picobj.getXMLNode(doc,'data',0)

g_osName = picobj.getOSName()
print g_osName

def getOScheckCmd():
		if g_osName == "ubuntu" or g_osName == "cos":
			return "dpkg -l "
		else:
			return "unknown "

def getAppFullName(name):
	if name == "wps":
		return "wps-office"
	elif name == "dia":
		return "dia"
	elif name == "evince" :
		return "evince"
	elif name == "firefox" :
		return "firefox"
	elif name == "iptux" :
		return "iptux"
	elif name == "thunderbird" :
		return "thunderbird"
	elif name == "filezilla" :
		return "filezilla"
	elif name == "cheese" :
		return "cheese"
	elif name == "gimp" :
		return "gimp"
	elif name == "xsane" :
		return "xsane"
	elif name == "brasero" :
		return "brasero"
	elif name == "eog" :
		return "eog"
	elif name == "audio-recorder" :
		return "audio-recorder"
	elif name == "smplayer" :
		return "smplayer"
	elif name == "rhythmbox" :
		return "rhythmbox"
	elif name == "nfs-securitycenter" :
		return "nfs-securitycenter"
	elif name == "nfs-antivirus" :
		return "nfs-antivirus"
	elif name == "nfs-firewall" :
		return "nfs-firewall"
	elif name == "mintupdate" :
		return "mintupdate"
	elif name == "aptdaemon" :
		return "aptdaemon"
	elif name == "gedit" :
		return "gedit"
	elif name == "gparted" :
		return "gparted"
	elif name == "nfs-screenshot" :
		return "nfs-screenshot"
	elif name == "nfs-file-compress" :
		return "nfs-file-compress"
	elif name == "nfs-phone-manager" :
		return "nfs-phone-manager"
	elif name == "lpmt" :
		return "lpmt"
	elif name == "system-config-printer-gnome" :
		return "system-config-printer-gnome"

def getAppCNName(name):
	if name == "wps":
		return "WPS"
	elif name == "dia":
		return u"Dia 图标绘制工具"
	elif name == "evince":
		return u"文档查看器"
	elif name == "firefox":
		return u"Firefox 火狐浏览器"
	elif name == "iptux":
		return u"Iptux 信使"
	elif name == "thunderbird":
		return u"Thunderbird 邮件客户端"
	elif name == "filezilla":
		return u"FileZilla FTP客户端"
	elif name == "cheese":
		return u"Cheese 摄像头工具"
	elif name == "gimp":
		return u"GIMP 图片编辑器"
	elif name == "xsane":
		return u"XSane 扫描仪工具"
	elif name == "brasero":
		return u"光盘刻录机"
	elif name == "eog":
		return u"图片查看器"
	elif name == "audio-recorder":
		return u"录音机"
	elif name == "smplayer":
		return u"Totem视频播放器/SMPlayer"
	elif name == "rhythmbox":
		return u"GNOME 音乐播放器"
	elif name == "nfs-securitycenter":
		return u"方德安全中心"
	elif name == "nfs-antivirus":
		return u"方德杀毒软件"
	elif name == "nfs-firewall":
		return u"方德防火墙"
	elif name == "mintupdate":
		return u"更新管理器"
	elif name == "aptdaemon":
		return u"软件中心"
	elif name == "gedit":
		return u"Gedit 编辑器"
	elif name == "gparted":
		return u"Gparted磁盘分析工具"
	elif name == "nfs-screenshot":
		return u"方德截图"
	elif name == "nfs-file-compress":
		return u"方德压缩"
	elif name == "nfs-phone-manager":
		return u"方德手机助手"
	elif name == "lpmt":
		return u"日志分析管理工具"
	elif name == "system-config-printer-gnome":
		return u"打印机"
	else:
		return ""


def main():
	commandHeader = getOScheckCmd()
	f=codecs.open( g_currentPath + picdir+'appVersions.txt','w','utf-8')
	f.write("ApplicationName\tVersion\n")
	app_count = 27
	for i in range(1, app_count):
				param = '%d' %i
				#get node name
				app_source = "app_source" + param
				name = "app_source_name" + param

				app_source = picobj.getXMLNode(data_node, name, 0)
				realname = picobj.getXMLNodeValue(app_source, 0)
				print realname

				commandline = commandHeader + " |grep " +"\" " + getAppFullName(realname) + " \"" + "| awk '{print $1 \" \" $2 \" \"  $3}' |awk '{print $3}'"
				print commandline

				#result = os.system(commandline)	
				p = subprocess.Popen(commandline,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
				(result,e) = p.communicate()
					
				if result == None:
					res = ""
				else :
					npos = result.find("ubuntu")
					if npos > 0:
						res = result[:npos-1]
					else:
						res = result
				print res

				content = '\t' + u"应用程序名: " + getAppCNName(realname) + '\n'
				f.write(content)
				res1 = res.strip('-')
				res2 = res1.strip('~')
				content1 = '\t' +  u"版本号: "+ res2 + '\n'
				f.write(content1)
	f.close()	
	return 

if __main__=="__main__":
	main()
