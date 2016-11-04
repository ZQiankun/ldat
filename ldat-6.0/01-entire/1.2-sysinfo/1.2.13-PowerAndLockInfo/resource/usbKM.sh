#!/bin/bash

if [ $# -ne 1 ] || [ "$1" != "enable" ] && [ "$1" != "disable" ]; then
	echo "Usage: $0 <enable | disable>"
	exit 1
fi

# ##########

if [ "$1" = "enable" ]; then
	while read LINE 
		do 
		for IF in $LINE
			do
			# echo $IF;
			echo $IF > /sys/bus/usb/drivers/usb/bind;
			done
		done < /tmp/usb
	exit 0
fi

if [ "$1" = "disable" ]; then
	USBIF=`ls /sys/bus/usb/drivers/usb | grep -`
	echo $USBIF > /tmp/usb
	for IF in $USBIF
		do
		# echo $IF;
		echo $IF > /sys/bus/usb/drivers/usb/unbind;
		done
	exit 0
fi

