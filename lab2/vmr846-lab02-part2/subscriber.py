import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, message):
	print("Received message: %s" % str(message.payload.decode("utf-8")))

broker = "0.0.0.0"
client = mqtt.Client("end_device")
client.connect(broker)

client.loop_start()
client.subscribe("DB_LEVEL")
client.on_message = on_message
time.sleep(30)
client.loop_end()
