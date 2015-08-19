#!/bin/bash
# What does it do:	Used to stop the HaaS & Network servers 
#			started by the accompanying script 
#			"startHaaSserver.sh"
# How to use it: 	Should be run from the same directory as
# 			the "startHaaSserver.sh" script

dir1=logs
cd $dir1

echo "** Stopping the HaaS server..."
echo " To abort press ^C in ... "
for i in $(seq 1 -1 0)
do
    echo -ne "$i sec\033[0K\r"
    sleep 1
done


for i in `cat pid_haas`
do
    pid1=`ps -ef |grep $i|grep haas|awk '{print $2 '}`
    if [ "$pid1" == "$i" ]
    then
	kill $i
    else
	echo "No haas service found running. Nothing to kill. :-("
	echo "Aborting. "
	exit 1
    fi
    
done

echo "HaaS servers stopped successfully "
> pid_haas



