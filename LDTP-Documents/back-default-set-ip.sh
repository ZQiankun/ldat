
IPCONFIG_PATH=/etc/network/
IPCONFIG_FILE=interfaces
IPCONFIG_FILE_BAK=interfaces.bak

if [ -f "$IPCONFIG_PATH/$IPCONFIG_FILE_BAK" ]; then
  mv $IPCONFIG_PATH/$IPCONFIG_FILE_BAK $IPCONFIG_PATH/$IPCONFIG_FILE
else
 ( echo  "# interfaces(5) file used by ifup(8) and ifdown(8)";
   echo  "auto lo";
   echo  "iface lo inet loopback") > $IPCONFIG_PATH/$IPCONFIG_FILE
fi

killall NetworkManager
