#include <Ethernet.h>
#include <PubSubClient.h>

#include "DHT.h"
#define DHT11_PIN 2

DHT dht11(DHT11_PIN, DHT11);
byte mac[] = {
  0xA8, 0x61, 0x0A, 0xAE, 0xA8, 0x91
};
IPAddress ip(10, 0, 56, 220);
IPAddress mqttServer(141, 147, 22, 203);

EthernetClient ethClient;
PubSubClient client(ethClient);

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message received on topic: ");
  Serial.println(topic);

  Serial.print("Payload: ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}

void setup() {
  Serial.begin(9600);
  dht11.begin(); // initialize the sensor

  Ethernet.begin(mac, ip);
  delay(1500);

  Serial.println("Connecting to MQTT broker...");
  client.setServer(mqttServer, 1883);
  client.setCallback(callback);

  while (!client.connected()) {
    if (client.connect("ArduinoClient")) {
      Serial.println("Connected to MQTT broker");
      client.subscribe("temperature");
    } else {
      Serial.print("Failed, rc=");
      Serial.print(client.state());
      Serial.println(" Retrying in 5 seconds...");
      delay(5000);
    }
  }

}

void publishMessage() {
  char message[50];
  sprintf(message, "Hello from Arduino at %lu", millis());

  client.publish("temperature", message); // topic, message
  Serial.println("Message published to MQTT broker");
}

void loop() {
  // wait a few seconds between measurements.
  delay(2000);

  // read humidity
  float humi  = dht11.readHumidity();
  // read temperature as Celsius
  float tempC = dht11.readTemperature();

  // check if any reads failed
  if (isnan(humi) || isnan(tempC)) {
    Serial.println("Failed to read from DHT11 sensor!");
  } else {
    Serial.print("DHT11# Humidity: ");
    Serial.print(humi);
    Serial.print("%");

    Serial.print("  |  "); 

    Serial.print("Temperature: ");
    Serial.print(tempC);
    Serial.print("°C ~ ");

    publishMessage();
  }


}
