#! /bin/bash

sh -c "sync && echo 3 > /proc/sys/vm/drop_caches"

if [ $# -eq 1 ]; then

	# 500M write
	echo "正在从主机硬盘拷贝500M数据到USB存储设备""$1"
	echo $1 | xargs -i dd if=/dev/zero of={}/usb_speed_test_file_500M bs=500M count=1 2>&1
	echo -e "主机硬盘拷贝到${1##*/} filename=usb_speed_test_file_500M bs=500M count=1\n"
	sh -c "sync && echo 3 > /proc/sys/vm/drop_caches"

	# 500M read
	echo "正在从USB存储设备""$1""拷贝500M数据到主机硬盘"
	echo $1 | xargs -i dd if={}/usb_speed_test_file_500M of=/dev/null bs=500M count=1 2>&1
	echo -e "${1##*/}拷贝到主机硬盘 filename=usb_speed_test_file_500M bs=500M count=1\n"
	echo $1 | xargs -i rm -rf {}/usb_speed_test_file_500M

	
	# 1G write
	echo "正在从主机硬盘拷贝1G数据到USB存储设备""$1"
	echo $1 | xargs -i dd if=/dev/zero of={}/usb_speed_test_file_1G bs=1G count=1 2>&1
	echo -e "主机硬盘拷贝到${1##*/} filename=usb_speed_test_file_1G bs=1G count=1\n"
	sh -c "sync && echo 3 > /proc/sys/vm/drop_caches"

	# 1G read
	echo "正在从USB存储设备""$1""拷贝1G数据到主机硬盘"
	echo $1 | xargs -i dd if={}/usb_speed_test_file_1G of=/dev/null bs=1G count=1 2>&1
	echo -e "${1##*/}拷贝到主机硬盘 filename=usb_speed_test_file_1G bs=1G count=1\n"
	echo $1 | xargs -i rm -rf {}/usb_speed_test_file_1G


	# 5G write
	echo "正在从主机硬盘拷贝5G数据到USB存储设备""$1"
	echo $1 | xargs -i dd if=/dev/zero of={}/usb_speed_test_file_5G bs=1G count=5 2>&1
	echo -e "主机硬盘拷贝到${1##*/} filename=usb_speed_test_file_5G bs=1G count=5\n"
	sh -c "sync && echo 3 > /proc/sys/vm/drop_caches"

	# 5G read
	echo "正在从USB存储设备""$1""拷贝5G数据到主机硬盘"
	echo $1 | xargs -i dd if={}/usb_speed_test_file_5G of=/dev/null bs=1G count=5 2>&1
	echo -e "${1##*/}拷贝到主机硬盘 filename=usb_speed_test_file_5G bs=1G count=5"
	echo $1 | xargs -i rm -rf {}/usb_speed_test_file_5G
fi

if [ $# -eq 2 ]; then
	OLD=$IFS
	IFS=$'\x0A'

	# 500M USB TO USB
	echo "正在准备500M数据"
	dd if=/dev/zero of=$1/usb_speed_test_file_500M bs=500M count=1 >/dev/null 2>&1
	sh -c "sync && echo 3 > /proc/sys/vm/drop_caches"
	echo "数据准备就绪"

	echo "正在从USB存储设备""$1""拷贝500M数据到USB存储设备""$2"
	dd if=$1/usb_speed_test_file_500M of=$2/usb_speed_test_file_500M bs=500M count=1 2>&1
	echo -e "${1##*/}拷贝到${2##*/} filename=usb_speed_test_file_500M bs=500M count=1\n"
	rm -rf $1/usb_speed_test_file_500M
	rm -rf $2/usb_speed_test_file_500M

	# 1G USB TO USB
	echo "正在准备1G数据"
	dd if=/dev/zero of=$1/usb_speed_test_file_1G bs=1G count=1 >/dev/null 2>&1
	sh -c "sync && echo 3 > /proc/sys/vm/drop_caches"
	echo "数据准备就绪"

	echo "正在从USB存储设备""$1""拷贝1G数据到USB存储设备""$2"
	dd if=$1/usb_speed_test_file_1G of=$2/usb_speed_test_file_1G bs=1G count=1 2>&1
	echo -e "${1##*/}拷贝到${2##*/} filename=usb_speed_test_file_1G bs=1G count=1\n"
	rm -rf $1/usb_speed_test_file_1G
	rm -rf $2/usb_speed_test_file_1G

	# 5G USB TO USB
	echo "正在准备5G数据"
	dd if=/dev/zero of=$1/usb_speed_test_file_5G bs=1G count=5 >/dev/null 2>&1
	sh -c "sync && echo 3 > /proc/sys/vm/drop_caches"
	echo "数据准备就绪"

	echo "正在从USB存储设备""$1""拷贝5G数据到USB存储设备""$2"
	dd if=$1/usb_speed_test_file_5G of=$2/usb_speed_test_file_5G bs=1G count=5 2>&1
	echo -e "${1##*/}拷贝到${2##*/} filename=usb_speed_test_file_5G bs=1G count=5\n"
	rm -rf $1/usb_speed_test_file_5G
	rm -rf $2/usb_speed_test_file_5G

	IFS=${OLD}
fi
