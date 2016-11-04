#!/bin/bash


num=0
while (($num <8))
do
	let "num++"
	gnome-screenshot -f ./screenshot/`date +%H%M%S`
done
	

