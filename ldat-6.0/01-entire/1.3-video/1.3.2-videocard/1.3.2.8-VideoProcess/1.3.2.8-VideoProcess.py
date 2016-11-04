#!/usr/bin/env python
#coding=utf-8

#########################################################################
# 1.3.2.8-VideoProcess.py
# Date: 2015/5/18
# Test Version: 
# Function: 
#########################################################################

import os
import sys
import time
import fcntl
import subprocess
import os.path
import platform

from ldtp import *

reload(sys)
sys.setdefaultencoding("utf8")

g_tag = "1.3.2.8-VideoProcess"
g_currentPath = sys.path[0]
g_publicLibPath = os.environ['AUTOTEST_PUBLIC_LIB']
sys.path.append(g_publicLibPath)


from logcase import Logcase
from caseobject import CaseObject

class Server(object):
    def __init__(self, cmd, server_env = None):
        if server_env:      
            self.process = subprocess.Popen(cmd,  shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=server_env)
        else:
            self.process = subprocess.Popen(cmd,  shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        flags = fcntl.fcntl(self.process.stdout, fcntl.F_GETFL)
        fcntl.fcntl(self.process.stdout, fcntl.F_SETFL, flags | os.O_NONBLOCK)
    def send(self, data, tail = '\n'):
        self.process.stdin.write(data + tail)
        self.process.stdin.flush()
    def recv(self, t=0.2, e=1, tr=10, stderr=0):
        #time.sleep(t)
        if tr < 1:
            tr = 1
        x = time.time() + t
        r = ''
        pr = self.process.stdout
        if stderr:
            pr = self.process.stdout
        while time.time() < x or r:
            try:    
                r = pr.read()
            except IOError:
                pass
                #print "Error: 没有可读的数据"
            else:
                pass
                #print "r:" + r
                        
            if r:
                break
            else:
                time.sleep(max((x - time.time())/tr, 0))
        return r.rstrip()
    def __del__(self):
        self.process.kill()
        self.process.wait()
        
    def parsel(self, re):
        dict_stats = {}
    
        lines = re.split("\n")
        if len(lines) <= 0 :
            return dict_stats
        for line in lines:
            #print "line: ", line
            line = line.strip('\r').strip()
            if line[0] == '|'  and len(line) > 2:
                tmp = line[2:]
                #print "tmp: ", tmp
                item = tmp.split(':')
                name = item[0].strip()
                value = item[1].strip()
                dict_stats[name] = value
                #print "name: %s, value: %s" % (name, value)
        return dict_stats
        
        
def runVlcPlayer(videoFile, outputFile):
    length = 0
    server = Server('sh\n')
    server.send("vlc \"%s\" -f --control rc" % videoFile)
    server.recv()
    # print "status:\n", server.recv()
    isplaying = 0
    
    outfile = open(outputFile, "w")
    outfile.write("%-20s%-20s%-20s%-20s\n" % ("TIME(second)", "FRAME DISPLAYED","FRAMES LOST","FRAME RATE"))
    server.send("")
    re = server.recv()
    while isplaying == 0:
        server.send("is_playing")
        re = server.recv()
        re =  re.strip('>').strip('\r').strip()
        if re: 
            strs = re.split("\n")
            try:
                isplaying = int(strs[0].strip('\r').strip()) 
            except ValueError:
                continue
    
    while length == 0:
        server.send("get_length")
        re = server.recv()
        re =  re.strip('>').strip('\r').strip()
        strs = re.split("\n")
        if len(strs) > 0: 
            try:
                length = int(strs[0].strip('\r').strip())
                #length = int('')
            except ValueError:
                print "length:%d" % length 
                continue
            
    
    while isplaying:    
        server.send("is_playing")
        re = server.recv()
        # print("re = %s" % re)
        re =  re.strip('>').strip('\r').strip()
        if re: 
            strs = re.split("\n")
            if len(strs) > 0:
                isplaying = int(strs[0].strip('\r').strip()) 
        if 0 == isplaying:
            break 

        server.send("get_time")
        re = server.recv()
        re =  re.strip('>').strip('\r').strip()
        strs = re.split("\n")
        if len(strs) > 0 :
            try:
                playtime = int(strs[0].strip('\r').strip())
            except ValueError:
                break
            if playtime == 0: 
                continue
        elif len(strs) == 0:
            break

        server.send("stats")
        re = server.recv()      
        dict_stats = server.parsel(re)
        #print "play time: %d" % playtime
        frame = int(dict_stats['frames displayed'])
        #print "frame:%d" % frame
        frame_rate = frame * 1.0 / playtime
        #print "frame rete: %f" % frame_rate
        frames_lost = dict_stats['frames lost']
        #print "frames_lost:" + frames_lost
        print "time: %d seconds, frames displayed %d, frames lost %s, frame rate %f." % (playtime, frame, frames_lost, frame_rate)
        outfile.write("%-20d%-20d%-20s%-20f\n" % (playtime, frame, frames_lost, frame_rate))

        time.sleep(0.5)
        server.send("is_playing")
        re = server.recv()
        # print("re = %s" % re)
        re =  re.strip('>').strip('\r').strip()
        if re: 
            strs = re.split("\n")
            if len(strs) > 0:
                isplaying = int(strs[0].strip('\r').strip()) 
        
    print "Play over."
    
    # 资源回收          
    server.send("q")
    time.sleep(0.2)
    server.send("exit")
    time.sleep(0.2)
    outfile.close()
                    
        

def main():
    
    # 读配置文件(xml文件）
    obj = CaseObject(g_tag, g_currentPath + '/' + g_tag + '.xml')
    doc = obj.getDocumentNode()
    commonNode = obj.getXMLNode(doc,'common',0)
    dataNode = obj.getXMLNode(doc,'data',0)
    
    resourcePath = g_currentPath + '/' + 'resource'
    osName = obj.getOSName()
    password = obj.getPasswd()
    arch = platform.architecture()[0]
    scriptDirname = resourcePath
    
    # 获得视频文件的文件名
    videoFileNode = obj.getXMLNode(dataNode, "video_file", 0)
    videoFile = obj.getXMLNodeValue(videoFileNode, 0)
    #print "videoFile:" + videoFile
    #videoFile =  os.path.abspath(videoFile)
  
#    videopath = os.path.expanduser(videoFile.strip())
    videopath = g_currentPath + videoFile
    
    # 判断文件是否存在
    if os.path.exists(videopath):
        if os.path.isfile(videopath) : 
            pass
        else :
            print "Video file does not exist."
            return
    else:
        print "Video file does not exist."
        return
    
    # 判断vlc是否已经安装
    hasVlc = os.system("which vlc")
    if hasVlc == 0 :
        # vlc 已经安装了
        print "VLC has been installed"
    else :  
        # 安装vlc
        if osName == 'ubuntu':
            print 'ubuntu'
            if arch == '64bit':
                scriptDirname = scriptDirname + "/vlc/vlc_ubuntu_64bit"
                os.chdir(scriptDirname)
                os.system("chmod a+x ./install.sh")
                os.system("./install.sh " + password)                  
            elif arch == '32bit':
                scriptDirname = scriptDirname + "/vlc/vlc_ubuntu_32bit"
                os.chdir(scriptDirname)
                os.system("chmod a+x ./install.sh")
                os.system("./install.sh " + password)
        elif osName == 'cos':
            print 'cos'
            if arch == '64bit':
                scriptDirname = scriptDirname + "/vlc/cos_64"
                os.chdir(scriptDirname)
                os.system("chmod a+x ./install.sh")
                os.system("./install.sh " + password)                  
            elif arch == '32bit':
                scriptDirname = scriptDirname + "/vlc/cos"
                os.chdir(scriptDirname)
                os.system("chmod a+x ./install.sh")
                os.system("./install.sh " + password)           
        elif osName == 'kylin':         
            if arch == '64bit':
                scriptDirname = scriptDirname + "/vlc/kylin/vlc-pkg-x86_64"
            elif arch == '32bit':
                scriptDirname = scriptDirname + "/vlc/kylin/vlc-pkg-i386"
            os.chdir(scriptDirname)
            os.system("chmod a+x ./install.sh")
            os.system("./install.sh " + password)
        elif osName == 'isoft':
            if arch == '64bit':
                pass
            elif arch == '32bit':
                scriptDirname = scriptDirname + "/vlc/iSoft"
                os.chdir(scriptDirname)
                os.system("chmod a+x ./install.sh")
                os.system("./install.sh " + password)
        else :
            pass
    
    outputFileNode = obj.getXMLNode(dataNode, "output_file", 0)
    outputFile = obj.getXMLNodeValue(outputFileNode, 0)
    outputFile = g_currentPath + "/result/" + outputFile
    os.chdir(resourcePath)
    runVlcPlayer(videopath, outputFile)

 
if __name__ == '__main__':
    main()
    
    
    
# 下面的这行语句用于清除屏幕
# os.system('''echo -e "\e[2J"''')

'''
    ---stats 命令返回的信息---
    
    +----[ begin of statistical info
    +-[Incoming]
    | input bytes read :     6719 KiB
    | input bitrate    :      455 kb/s
    | demux bytes read :     5850 KiB
    | demux bitrate    :      336 kb/s
    | demux corrupted  :        0
    | discontinuities  :        0
    |
    +-[Video Decoding]
    | video decoded    :     2528
    | frames displayed :     2511
    | frames lost      :        4
    |
    +-[Audio Decoding]
    | audio decoded    :     4941
    | buffers played   :     4941
    | buffers lost     :        2
    |
    +-[Streaming]
    | packets sent     :        0
    | bytes sent       :        0 KiB
    | sending bitrate  :        0 kb/s
    +----[ end of statistical info ]
'''


