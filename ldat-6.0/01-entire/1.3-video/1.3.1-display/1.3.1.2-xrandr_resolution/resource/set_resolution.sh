#!/bin/bash
#Author: lenovo
#version: 0.1

#获取默认的分辨率
NorMAL=`xrandr -q | awk '{ if( $1 ~ /[0-9]{1,}x[0-9]{1,}/) {print $1}}' | head -1`
#获取默认的输出端口
OutPut=`xrandr -q | awk '$2=="connected" {print $1} '`

#设置默认的分辨率
xrandr  --output $OutPut --mode $NorMAL
sleep 5

