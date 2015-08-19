#!/bin/bash
# What does it do: 	Starts HaaS and Network server in background
#		   	Output is logged to file in ./logs folder
# How to use it:	Move the scripts to the folder same as the one
#			having haas.cfg
# 			or 
#			HaaS command line should be suitably exported into its path
# To stop server another script "stopHaaSserver.sh" should be used


dir1=`pwd`/logs
echo `pwd`
h_server="haas_server_`date +%F`.log"
n_server="haas_networkQ_`date +%F`.log"

echo "** Starting the HaaS server **"
haas serve 5001 >> $dir1/$h_server 2>&1 & 
PID1=`echo $!`
sleep 2

PID2=`ps -ef |grep $PID1|grep haas|awk '{print $2 '}`

if [ "$PID1" == "$PID2" ]
then
    echo $PID1 > $dir1/pid_haas
    echo " Server started successfully "
    echo " Output logged in "$h_server" "
    jobs
    sleep 2 
    echo " "
    echo " Starting the network server"
    haas serve_networks > $dir1/$n_server 2>&1 & 
    PID3=`echo $!`
    sleep 2

    PID4=`ps -ef |grep $PID3|grep haas|awk '{print $2 '}`

    if [ "$PID3" == "$PID4" ]
    then
	echo $PID3 >> $dir1/pid_haas
	echo " Network server started successfully "
	echo " Output being logged to "$n_server" "
	jobs
    else
	echo "Error: Network server failed to start. "
	echo " Aborting. "; exit 1
    fi 
else
    echo " Error: HaaS server did not start as expected "
    exit 1
fi
