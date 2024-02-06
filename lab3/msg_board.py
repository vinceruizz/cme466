import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, message):
	data = str(message.payload.decode("utf-8"))
	print("[MSG_BOARD] Received message: %s" % str(data))

broker = "broker.hivemq.com"
client = mqtt.Client("end_device")
client.connect(broker)

client.loop_start()
client.subscribe("DB_LEVEL") # you can change the QoS by adding parameter qos=x (replace x with desired QoS level (0, 1, 2)
client.on_message = on_message
time.sleep(30)
client.loop_end()
