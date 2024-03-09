#!/bin/bash

while :
do
	TEMP="$(cat ~/FTP/share/www/assets/temperature.txt)"
	mosquitto_pub -h 141.147.22.203 -t "temperature" -m "Trutnov:$TEMP"
	sleep 300
done
