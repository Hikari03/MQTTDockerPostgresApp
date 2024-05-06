# Temperature information collection

## Description

This project aims to collect temperature information from devices and use MQTT broker
to send the information to a server that is subscribed to the broker.

This means that you can have multiple devices sending temperature information and
multiple servers receiving this information.

## Technology

Temperature is measured using raspberry pi and is published to an MQTT broker via bash script.

The server is subscribed to the MQTT broker and receives the temperature information.
The server is written in python and data is stored in a postgres database.

The broker as well as the server are containerized using docker.

### Scheme
![obrazek](https://github.com/aldudkin/MQTTDockerPostgresApp/assets/39591367/71ee3f14-0a58-4f36-b702-5db2c770dee4)


## How to run

### Broker

#### Dependencies
- `docker`
- `docker-compose` if `docker compose` command is not available => use `docker-compose` instead of `docker compose`
- make sure that the port 1883 is open for connections

#### How to run
```
git clone git@github.com:aldudkin/MQTTDockerPostgresApp.git         # Clone the repository
cd MQTTDockerPostgresApp/mqttbroker                                 # Go to the broker directory
docker compose up -d                                                # Run the broker
```

By default, there should be already user `temperature` with password `varilamysickakasicku`.
However, if you want to create a new user, you can do so by following these steps:

First, enter the container shell:
```
docker compose exec mosquitto sh                                    # Enter the container shell
```

Then, in container shell:
```
chmod 0700 /mosquitto/config/pwfile                                 # Change permissions of the password file
chown root /mosquitto/config/pwfile                                 # Change owner of the password file
mosquitto_passwd -c /mosquitto/config/pwfile <USERNAME>             # Create a new user
exit
```

Finally, restart the container:
```
docker compose restart mosquitto
```

#### Test
```
mosquitto_sub -h "<BROKER_IP>" -t "<TOPIC>" -u "<USERNAME>" -P "<PASSWORD>"
# Subscribes to the TOPIC topic
```

And in a separate terminal:
```
mosquitto_pub -h "<BROKER_IP>" -t "<TOPIC>" -m "<MESSAGE>" -u "<USERNAME>" -P "<PASSWORD>"
# Publishes a MESSAGE to the TOPIC topic
# Password is the one you created with mosquitto_passwd
```

Now you should see the message you published in the first terminal.


### Server

#### Dependencies
- `docker`
- `docker-compose` if `docker compose` command is not available => use `docker-compose` instead of `docker compose`

#### How to run
```
git clone git@github.com:aldudkin/MQTTDockerPostgresApp.git         # Clone the repository
cd MQTTDockerPostgresApp/endpoint                                   # Go to the server directory 
docker compose up -d                                                # Run the server
```

To test the server, you can use the following command:


The server is using the `temperature` topic in MQTT by default.

#### Test
```
mosquitto_pub -h "<BROKER_IP>" -t "temperature" -m "<LOCATION>:<TEMP>[.<DECIMAL>]°C" -u <USERNAME> -P <PASSWORD>
# Password is the one you created with mosquitto_passwd
```

To check the data in the database, you can use the following command:
```
docker exec -it endpoint-postgres sh
```

Then, in container shell:
```
psql -U postgres -d temperature_data -c "select * from temperature_data"
```

### Sensor Device

#### Dependencies
- `mosquitto`

#### How to run
All the sensor device needs to do is to run the bash script that sends the temperature information to the broker.
Example of the script is provided in the `data-send-scripts` directory.

