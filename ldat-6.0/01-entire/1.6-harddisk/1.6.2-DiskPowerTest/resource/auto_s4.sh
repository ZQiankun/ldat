#!/bin/bash

path=`pwd`
echo  "The current path is:"
echo $path

pass=$2
echo "Your passwd is "
echo $pass

NUM=$1
if [ "x$1x" = "xx" ]
then 
	echo "error : 请输入要休眠的次数 ........ "
	exit 1
fi
echo "系统将 进行 休眠  $1 次"
#这条测试S4挂起到磁盘
while [ $NUM -gt 0 ]
do
	cnum=`expr $1 - $NUM + 1`
	echo "这将进行  第 $cnum 次"
			sync
		sync
	sleep 30
	echo $pass  | sudo -S sh -c "echo \"rtcwake S4 `date`\" >> ./result/Disk_AfterS4.log"
	rtcwake -m disk -s 120
	NUM=`expr $NUM - 1`
done

exit 0

