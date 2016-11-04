# coding=utf-8

import hashlib
import time
import os
import sys
import random
import struct
import shutil

sys.path.append(os.environ['AUTOTEST_PUBLIC_LIB'])
from logcase import Logcase
from caseobject import CaseObject
import udisk_information


def get_md5_for_file(filename):
    m = hashlib.md5()
    with open(filename, 'rb') as fp:
        while True:
            blk = fp.read(4096)  # 4KB per block
            if not blk: break
            m.update(blk)
    return m.hexdigest()


class Log():
    def __init__(self, logfile):
        self.logfile = logfile

    def open(self):
        self.stream = open(self.logfile, "a+")

    def appenddatetime(self):
        current_time = time.strftime("%Y-%m-%d %X", time.localtime(time.time()))
        self.stream.write(current_time + "\n")

    def appendline(self, line):
        self.stream.write("%s\n" % line)

    def close(self):
        self.stream.flush()
        self.stream.close()


def get_s4_is_enable():
    return int(os.environ['S4_ENABLE'])

def get_s3_is_enable():
    return int(os.environ['S3_ENABLE'])


def main():
    reload(sys)
    sys.setdefaultencoding('utf8')
    current_path = sys.path[0]
    current_datetime = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))

    tag = "1.9.2-usbreadwrite"
    obj = CaseObject(tag, current_path + '/1.9.2-usbreadwrite.xml')
    doc = obj.getDocumentNode()
    g_osName = obj.getOSName()
    password = obj.getPasswd()

    # 读配置文件
    data_node = obj.getXMLNode(doc, 'data', 0)
    tmp_node = obj.getXMLNode(data_node, "output", 0)
    output_file = obj.getXMLNodeValue(tmp_node, 0)
    output_file = output_file.strip()
    output_file = os.path.join(current_path, "result", output_file)
    g_log = Logcase()
    output = Log(output_file)
    output.open()
    output.appenddatetime()

    def error_log_and_print(error_str):
        g_log.elog(tag, error_str)
        print(error_str)

    # 生成一个10M的随机文件
    random_file = os.path.join(current_path, current_datetime)
    md5_value = ""
    try:
        in_stream = open(random_file, "a+")
    except IOError:
        error_log_and_print("Failed to open file")
        return

    # generate 10MB random file.
    size = 10 * 1024 * 1024
    count = size
    minint = -sys.maxint - 1
    maxint = sys.maxint
    # start_time = time.time()
    while count > 0:
        r = random.randint(minint, maxint)
        bytes = struct.pack('l', r)
        in_stream.write(bytes)
        count -= len(bytes)
    in_stream.close()
    # print("time: ", time.time() - start_time)

    md5_value = get_md5_for_file(random_file)
    output.appendline("source file md5 value is: %s" % md5_value)
    print("md5_value", md5_value)
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

    mount_point_list = []
    # 获得挂载点列表
    for d in usb3_0_devices + usb2_0_devices:
        mount_point = d["mount_point"]
        avail_size = d["avail"] * 1024
        if (avail_size < size * 3):
            error_log_and_print(mount_point + ": There is not enough space in usb storage device.")
        else:
            mount_point_list.append(mount_point)

    if 0 == len(mount_point_list):
        error_log_and_print("Did not plug in usb storage device.")
        output.appendline("-" * 10 + "Did not plug in usb storage device." + "-" * 10)

    def copy_random_file(i):
        # print(mount_point_list)
        for mount_point in mount_point_list:
            # host -> mount_point
            src = random_file
            basename = os.path.basename(random_file)
            dst = os.path.join(mount_point, basename + str(i))
            try:
                shutil.copyfile(src, dst)
            except IOError:
                error_log_and_print("host --> %s  copy error (IOError)" % mount_point)
            else:
                md5_value_dst = get_md5_for_file(dst)
                if md5_value == md5_value_dst:
                    s = "host --> %s copy, md5 values is:\n    %s\n    OK" \
                        % (mount_point, md5_value_dst)
                    output.appendline(s)
                    print(s)
                else:
                    s = "host --> %s copy, md5 values is:\n    %s\n    Error" \
                        % (mount_point, md5_value_dst)
                    output.appendline(s)
                    print(s)

            # mount_point -> host
            src = dst
            host_dirname = os.path.dirname(random_file)
            mp_basename = os.path.basename(dst)
            dst = os.path.join(host_dirname, mp_basename)
            # print("src:", src, "\ndst:", dst)
            try:
                shutil.copyfile(src, dst)
            except IOError:
                error_log_and_print("%s --> host copy file error (IOError)" % mount_point)
            else:
                md5_value_dst = get_md5_for_file(dst)
                if md5_value == md5_value_dst:
                    s = "%s --> host copy, md5 values is:\n    %s\n    OK" \
                        % (mount_point, md5_value_dst)
                    output.appendline(s)
                    print(s)
                else:
                    s = "%s --> host copy, md5 values is:\n    %s\n    Error" \
                        % (mount_point, md5_value_dst)
                    output.appendline(s)
                    print(s)

            try:
                os.remove(dst)
            except IOError:
                error_log_and_print("host -- delete file failed.")
            try:
                os.remove(src)
            except IOError:
                error_log_and_print("%s -- delete file failed." % mount_point)

    # 测试S3 S4
    modes = ["s3", "s4"]
    for mode in modes:
        for i in range(3):
            if mode == 's3':
                s3_is_enable = get_s3_is_enable()
                if s3_is_enable == 1:
                    os.system('echo ' + password + ' | sudo -S rtcwake -m mem -s 120')
                    print('s3')
                    time.sleep(10)
                    copy_random_file(i)
                else:
                    s = "-" * 10 + "S3 disable." + "-" * 10
                    output.appendline(s)
                    print(s)
            if mode == 's4':
                s4_is_enable = get_s4_is_enable()
                if s4_is_enable == 1:
                    os.system('echo ' + password + ' | sudo -S rtcwake -m disk -s 120')
                    print('s4')
                    time.sleep(10)
                    copy_random_file(i)
                else:
                    s = "-" * 10 + "S4 disable." + "-" * 10
                    output.appendline(s)
                    print(s)

    # delete random file
    try:
        os.remove(random_file)
        # print("delete random file")
    except IOError:
        error_log_and_print("host -- delete random file failed.")

    output.appendline("-" * 32 + "END" + "-" * 32 + "\n" * 2)
    output.close()



if __name__ == '__main__':
    main()
