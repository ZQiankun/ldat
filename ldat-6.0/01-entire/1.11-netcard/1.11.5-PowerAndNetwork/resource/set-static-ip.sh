#!/bin/bash
IPCONFIG_PATH=/etc/network/
IPCONFIG_FILE=interfaces
IPCONFIG_FILE_BAK=interfaces.bak
NETWORKPATH=/etc/NetworkManager/
NETDIRNAME=system-connections
NETDIRNAMEM=system-connections-bak

        if [ ! -f "$IPCONFIG_PATH/$IPCONFIG_FILE_BAK" ]; then
                echo "${1}" | sudo -S mv $IPCONFIG_PATH/$IPCONFIG_FILE $IPCONFIG_PATH/$IPCONFIG_FILE_BAK
        else
                echo "static ip has configed"
                return
        fi

        echo "${1}" | sudo -S sh -c "cat $IPCONFIG_PATH/$IPCONFIG_FILE_BAK > $IPCONFIG_PATH/$IPCONFIG_FILE"
        echo "${1}" | sudo -S sh -c "(echo  \"auto eth0\";
         echo  \"iface eth0 inet static\";
         echo  \"address 192.168.0.12\";
         echo  \"gateway 192.168.0.1\";
         echo  \"netmask 255.255.255.0\";
         echo  \"broadcast 192.168.0.255\" ) >> $IPCONFIG_PATH/$IPCONFIG_FILE"

#if [ -d "$NETWORKPATH/$NETDIRNAME" ]; then
#  mv $NETWORKPATH/$NETDIRNAME $NETWORKPATH/$NETDIRNAMEM
#fi
        echo "${1}" | sudo -S killall NetworkManager

        echo "${1}" | sudo -S ifdown --force eth0
        sleep 2
        echo "${1}" | sudo -S ifup --force eth0

        if [ $? -eq 0 ]; then
                echo  "Config static ip ok";
                ifconfig eth0
        else
                echo  "Config Failed!Please try a again";
        fi
