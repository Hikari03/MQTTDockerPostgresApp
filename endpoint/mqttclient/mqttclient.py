# python3.6

import random
from time import sleep

from paho.mqtt import client as mqtt_client
from psycopg2 import connect, Error
from datetime import datetime


logFile = open("log.txt", "w")


def log(message):
    print(str(datetime.now()) + ": " + message)
    logFile.write(str(datetime.now()) + ": " + message + "\n")
    logFile.flush()


broker = 'mqttbroker.houdeda2.cz'
port = 1883
topic = "temperature"
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
username = 'temperature'
password = 'varilamysickakasicku'

sleep(10)

# DB connection
connection = connect(
    dbname="temperature_data",
    host="db",
    user="postgres",
    password="varilamysickakasicku"
)

log("Database opened successfully")
cursor = connection.cursor()

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            log("Connected to MQTT Broker!")
        else:
            log("Failed to connect, return code " + rc)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def on_message(client, userdata, msg):
    mess = msg.payload.decode().split(":", 1)
    location = mess[0]
    try:
        temp = float(mess[1].strip("°C"))
    except ValueError:
        log(f"Temperature is not a number: {mess[1]}")
        return

    if location == "":
        log("Location is empty")
        return

    if temp == "":
        log("Temperature is empty")
        return

    try:
        cursor.execute("INSERT INTO temperature_data (location, temperature_celsius, measurement_date) VALUES (%s, %s, "
                       "now())", (location, temp))
        connection.commit()
        log(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        log(f"Location: {location}, Temperature: {temp}")
    except Error as e:
        log(f"Error: {e}")
        return


def subscribe(client: mqtt_client):
    log(f"Subscribing to topic `{topic}`")
    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


# def create_table():
#    try:
#        cursor.execute("CREATE TABLE IF NOT EXISTS temperature_data (id SERIAL PRIMARY KEY, location VARCHAR(255), temperature_celsius FLOAT, measurement_date TIMESTAMP)")
#        connection.commit()
#        cursor.execute("SELECT 1 FROM temperature_data")
#        log("Table created successfully")
#    except Exception as e:
#        log(f"Error: {e}")


if __name__ == '__main__':
   # create_table()
    run()



