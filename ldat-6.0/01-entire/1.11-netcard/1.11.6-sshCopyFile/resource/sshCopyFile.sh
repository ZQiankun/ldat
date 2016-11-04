#!/bin/bash

#$1:source_path  $2:destination_path  $3:another_host_passward  $4:expect_path  $5:host_passward

isexpect=`which expect`

if [ "$isexpect" != "" ]; then
    echo "expect installed!"
else    
	echo $5 | sudo -S dpkg -i $4
	sleep 3
fi

expect -c "
spawn scp $1 $2
expect {
    \"*assword\" {set timeout 300; send \"$3\r\";}
    \"yes/no\" {send \"yes\r\";}
      }
expect eof"

