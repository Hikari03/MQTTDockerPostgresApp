# python3.6

import random

from paho.mqtt import client as mqtt_client
from psycopg2 import connect, Error

broker = 'mqttbroker.houdeda2.cz'
port = 1883
topic = "temperature"
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
username = 'temperature'
password = 'varilamysickakasicku'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def on_message(client, userdata, msg):
    msg.split(":", 1)
    location = msg[0]
    temp = msg[1]

    if location.empty:
        print("Location is empty")
        return

    if temp.empty:
        print("Temperature is empty")
        return

    try:
        connection = connect(
            dbname="temperature",
            host="localhost",
            user="temperature",
            password="varilamysickakasicku"
        )
        cursor = connection.cursor()
        cursor.execute("INSERT INTO temperature (location, temperature) VALUES (%s, %s)", (location, temp))



def subscribe(client: mqtt_client):
    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()


