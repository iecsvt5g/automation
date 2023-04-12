#!/bin/sh

:<<BLOCK
Created on 2023/04/12
Modified on 2023/04/13
@author: ZL Chen
@title: Precondition Setting
BLOCK

function clean_log() {
	echo "" > /root/check_time.log
}

function version_check() {
	if [[ $1 == "29" ]]
	then
		eeprom-tools -t $1 -r | grep uptime >> /root/check_time.log 2>&1
		echo "eeprom-tools -t $1 -r | grep uptime"
	fi
	if [[ $2 == mmcblk1p* ]] && [[ $3 == mmcblk1p* ]] 
	then
		lsblk | grep $2 >> /root/check_time.log 2>&1
		lsblk | grep $3 >> /root/check_time.log 2>&1
		echo "lsblk | grep $2, lsblk | grep $3"
	fi
}

function routing() {
	if [[ $1 = */* ]] && [[ $2 = *.*.*.* ]]
	then
		/sbin/route del -net $1 gw $2 >> /root/check_time.log 2>&1
		echo "/sbin/route del -net $1 gw $2 >> /root/check_time.log 2>&1"
		sleep 1
		/sbin/route add -net $1 gw $2 >> /root/check_time.log 2>&1
		echo "/sbin/route add -net $1 gw $2 >> /root/check_time.log 2>&1"
		sleep 1
		echo "Add routing $1 gw $2"
	else
		echo "Add routing $1 gw $2 Error"
	fi
	sync
}

function routing_gateway_check() {
	if [[ $1 = *.*.*.* ]]
	then
		route -n | grep $1
		echo "route -n | grep $1"
	else
		echo "route -n | grep $1 Error"
	fi
	sync
}

function main() {
	sleep 120
	#sleep 1
	clean_log
	version_check "29" "mmcblk1p2" "mmcblk1p5"
	routing "0.0.0.0/0" "172.32.3.5"
	routing "192.168.99.0/24" "172.32.3.5"
	routing "172.32.4.0/24" "172.32.3.5"
	routing_gateway_check "172.32.3.5"
}

main
echo "Finished"