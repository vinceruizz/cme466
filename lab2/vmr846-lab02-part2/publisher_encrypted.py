import paho.mqtt.client as mqtt
import time
from random import randrange, uniform
import ntplib
import json

broker = "0.0.0.0"
client = mqtt.Client("client1")
client.connect(broker)

def getTime():
	ntpClient = ntplib.NTPClient()
	try:
		result = ntpClient.request("pool.ntp.org")
		time = result.tx_time
		print(f"Initial time: {time}")
		return time
	except Exception as e:
		print(f"Error with NTP. Got: {e}")


while True:
	randNum = uniform(20.0,21.0)
	initialTime = getTime()
	msg = {"data":randNum,"timestamp":initialTime}
	payload = json.dumps(msg)
	client.publish("DB_LEVEL", payload, qos=0, retain=True) # To change the QoS level, edit the qos arguemnt with the desired QoS level (0,1,2). To set/clear the retain flag, change the retain parameter to True/False, respectively
	print("[PUBLISHER] Just published %s to topic \"DB_LEVEL\"" % json.loads(payload))
	time.sleep(1) 
