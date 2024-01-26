import paho.mqtt.client as mqtt
import time
from random import uniform

broker = "0.0.0.0"
client = mqtt.Client("client1")
client.connect(broker)

while True:
    randNum = uniform(0,100)
    client.publish("DB_LEVEL", randNum, qos=0, retain=True) # To change the QoS level, change the argument "2" to your desired QoS level. To set/clear the retain flag, change the "True" argument
    print("Just published %s to topic \"DB_LEVEL\"" % str(randNum))
    time.sleep(1)
    
