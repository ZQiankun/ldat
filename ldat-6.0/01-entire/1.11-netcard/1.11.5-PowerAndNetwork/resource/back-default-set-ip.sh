
IPCONFIG_PATH=/etc/network/
IPCONFIG_FILE=interfaces
IPCONFIG_FILE_BAK=interfaces.bak

if [ -f "$IPCONFIG_PATH/$IPCONFIG_FILE_BAK" ]; then
  	echo "${1}" | sudo -S mv $IPCONFIG_PATH/$IPCONFIG_FILE_BAK $IPCONFIG_PATH/$IPCONFIG_FILE
else
  echo "${1}" | sudo -S echo  "# interfaces(5) file used by ifup(8) and ifdown(8)" >> $IPCONFIG_PATH/$IPCONFIG_FILE
  echo "${1}" | echo  "auto lo" >> $IPCONFIG_PATH/$IPCONFIG_FILE
  echo "${1}" | echo "iface lo inet loopback" >> $IPCONFIG_PATH/$IPCONFIG_FILE
fi

echo "${1}" | sudo -S killall NetworkManager
