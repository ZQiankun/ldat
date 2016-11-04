
#!/bin/bash
if [ $# -ne 1 ]; then
	echo "Arguments Error; Usage: $0 <password>"
	exit 1
fi 
password=$1


echo "$password" | sudo -S dpkg -i *.deb

