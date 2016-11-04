# coding=utf-8
import time
import os
import sys
import os.path
import shutil
import commands
import shutil
from ldtp import *

sys.path.append(os.environ['AUTOTEST_PUBLIC_LIB'])
from logcase import Logcase
from caseobject import CaseObject
import udisk_information
from screenshot import Screenshot
g_currentPath = sys.path[0]
g_sst = Screenshot()
g_log = Logcase()


def main():
    reload(sys)
    sys.setdefaultencoding('utf8')
    # 读配置文件
    tag = "1.9.6-playvideo_with_udisk"
    obj = CaseObject(tag, g_currentPath + '/1.9.6-playvideo_with_udisk.xml')
    doc = obj.getDocumentNode()
    g_osName = obj.getOSName()

    data_node = obj.getXMLNode(doc, 'data', 0)
    tmp_node = obj.getXMLNode(data_node, "video_resource_name", 0)
    video_file = obj.getXMLNodeValue(tmp_node, 0)
    video_file = video_file.strip()
    video_file = os.path.expanduser(video_file)

    tmp_node = obj.getXMLNode(data_node, "video_play_time", 0)
    play_time = obj.getXMLNodeValue(tmp_node, 0)

    def error_log_and_print(error_str):
        g_log.elog(tag, error_str)
        print(error_str)

    # 获得usb存储设备
    timeout = time.time() + 60
    while time.time() < timeout:
        usb2_0_devices, usb3_0_devices = udisk_information.get_usb_storage_information()
        if (usb2_0_devices is None) or (usb3_0_devices is None):
            time.sleep(1)
        else:
            break
    else:
        error_log_and_print("Get usb storage devices information is failure.")
        return

    if len(usb3_0_devices) == 0:
        error_log_and_print("No usb 3.0 storage device.")
        return

    # 验证视频文件
    if not os.path.exists(video_file):
        error_log_and_print("Not found video file.")
    elif not os.path.isfile(video_file):
        error_log_and_print("Not regular file.")

    # 获得视频文件的size
    video_size = os.path.getsize(video_file)

    mount_point = ""
    # 找到一个usb 3.0的u盘或移动硬盘
    for d in usb3_0_devices:
        avail_size = d["avail"] * 1024
        if (avail_size > video_size):
            mount_point = d["mount_point"]
            break
    else:
        error_log_and_print("There is not enough space in usb storage device.")
        return

    # 拷贝文件
    timestamp = int(time.time())
    basename = os.path.basename(video_file)
    dst = os.path.join(mount_point, str(timestamp) + basename)
    try:
        shutil.copyfile(video_file, dst)
    except IOError:
        error_log_and_print("Copy file error.")
        return

    for i in range(2):
        player = ""
        command_str  = ""
        if g_osName == 'kylin':
            player = "smplayer"
            command_str = 'smplayer "%s" &' % dst
        elif g_osName == 'cos' or g_osName == 'isoft':
            player = "totem"
            command_str = 'totem "%s" &' % dst
        else:
            error_log_and_print("Unsupported file system.")
            return

        status = os.system(command_str)
        if status != 0:
            error_log_and_print("Play video error")
            return

        time.sleep(play_time)
        # 截屏
        g_sst.scrprint('1.9.6-playvideo_with_usb', 'usb' , g_currentPath)
        closewindow(dst)
        time.sleep(2)
        os.system("killall %s 1>/dev/null 2>/dev/null &" % player)
        time.sleep(2)

if __name__ == '__main__':
    main()
