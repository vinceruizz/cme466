import paho.mqtt.client as mqtt
import time
from random import randrange, uniform

broker = "192.168.2.2"
client = mqtt.Client("client1")
client.connect(broker)

while True:
    randNum = uniform(20.0,21.0)
    client.publish("DB_LEVEL", randNum)
    print("Just published %s to topic \"DB_LEVEL\"")
    time.sleep(1)
    