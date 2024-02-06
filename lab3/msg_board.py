import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, message):
	data = str(message.payload.decode("utf-8"))
	print("[MSG_BOARD] Received message: %s" % str(data))

broker = "broker.hivemq.com"
client = mqtt.Client("msg_board_client_ruiz")
client.connect(broker)

client.loop_forever()
client.subscribe("MSG_BOARD") # you can change the QoS by adding parameter qos=x (replace x with desired QoS level (0, 1, 2)
client.on_message = on_message

while True:
	end_connection = input(">> ")
	if end_connection == "end":
		client.disconnect()