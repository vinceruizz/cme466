import paho.mqtt.client as mqtt
import time
import ntplib
import json

def on_message(client, userdata, message):
	received = json.loads(message.payload.decode("utf-8"))
	data = received["data"]
	initialTime = received["timestamp"]
	print("[SUBSCRIBER] Received message: %s" % str(data))

	ntpClient = ntplib.NTPClient()
	try:
		currentTime = (ntpClient.request("pool.ntp.org")).tx_time
		latency = (currentTime - initialTime) * 1000
		print(f'[SUBSCRIBER] Transmission latency: {latency}')
	except Exception as e:
		print(f'Error with NTP. Got: {e}')

broker = "0.0.0.0"
client = mqtt.Client("end_device")
client.connect(broker)

client.loop_start()
client.subscribe("DB_LEVEL") # you can change the QoS by adding parameter qos=x (replace x with desired QoS level (0, 1, 2)
client.on_message = on_message
time.sleep(30)
client.loop_end()
