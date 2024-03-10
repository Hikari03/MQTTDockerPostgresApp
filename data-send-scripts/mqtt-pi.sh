#!/bin/bash

while :
do
	TEMP="$(cat ~/FTP/share/www/assets/temperature.txt)"
	mosquitto_pub -h mqttbroker.houdeda2.cz -t "temperature" -m "Trutnov:$TEMP" -u "temperature" -P "varilamysickakasicku"
	sleep 300
done
