#! /bin/bash

# $1 = add or rm\
# $2 = mountPoint
# $3 = datasize


if [ $1 = "add" ]; then
	if [ $3 = "500M" ]; then
		echo "准备500M数据..."
		echo $2 | xargs -i dd if=/dev/zero of={}/copy_data_test_file_500M bs=500M count=1 >/dev/null 2>/dev/null
	fi
	if [ $3 = "1G" ]; then
		echo "准备1G数据..."
		echo $2 | xargs -i dd if=/dev/zero of={}/copy_data_test_file_1G bs=1G count=1 >/dev/null 2>/dev/null
	fi
	if [ $3 = "2G" ]; then
		echo "准备2G数据..."
		echo $2 | xargs -i dd if=/dev/zero of={}/copy_data_test_file_2G bs=1G count=2 >/dev/null 2>/dev/null
	fi
	if [ $3 = "5G" ]; then
		echo "准备5G数据..."
		echo $2 | xargs -i dd if=/dev/zero of={}/copy_data_test_file_5G bs=1G count=5 >/dev/null 2>/dev/null
	fi

	sh -c "sync && echo 3 > /proc/sys/vm/drop_caches"
fi


if [ $1 = "rm" ]; then

	if [ $3 = "500M" ]; then
		echo $2 | xargs -i rm -rf {}/copy_data_test_file_500M
	fi
	if [ $3 = "1G" ]; then
		echo $2 | xargs -i rm -rf {}/copy_data_test_file_1G
	fi
	if [ $3 = "2G" ]; then
		echo $2 | xargs -i rm -rf {}/copy_data_test_file_2G
	fi
	if [ $3 = "5G" ]; then
		echo $2 | xargs -i rm -rf {}/copy_data_test_file_5G
	fi
fi
	
