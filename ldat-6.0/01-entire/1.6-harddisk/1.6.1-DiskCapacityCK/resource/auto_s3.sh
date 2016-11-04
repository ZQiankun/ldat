#!/bin/bash

NUM=$1
if [ "x$1x" = "xx" ]
then 
	echo "error : 请输入要执行的次数 ........ "
	exit 1
fi
echo "系统将 进行 睡眠  $1 次"
#这条测试S3挂起到内存
while [ $NUM -gt 0 ]
do
	cnum=`expr $1 - $NUM + 1`
	echo "这将进行  第 $cnum 次"
	sleep 20
	rtcwake -m mem -s 10
	NUM=`expr $NUM - 1`
done


