import paho.mqtt.client as mqtt
import threading
import json
import time

def on_message(client, userdata, message):
    payload = json.loads(message.payload)
    type = payload["type"]
    data = payload["data"]
    if type == "msg_board":
        print(f"[{type}] Received message: {str(data)}")

broker = "broker.hivemq.com"
client = mqtt.Client("msg_board_client_ruiz")
client.connect(broker)


client.loop_start()
client.subscribe("MSG_BOARD") # you can change the QoS by adding parameter qos=x (replace x with desired QoS level (0, 1, 2)
client.on_message = on_message

def manage_connection():
    while True:
        manage_connection = input(">> ")
        if manage_connection == "end":
            client.loop_stop()
            print("connection to broker ended")
        if manage_connection == "start":
            client.loop_start()
            print("connection to broker started")

def simulate_parking():
    dataset = [
        [True, False, True, True, True],
        [False, True, True, False, False],
        [True, False, True, False, False],
        [False, True, False, False, True],
        [False, False, True, True, False],
        [False, False, False, False, False],
        [True, False, False, True, True],
        [False, False, True, False, False],
        [False, True, True, False, True],
        [False, True, True, False, False],
        [False, True, True, False, True],
        [True, False, True, True, True],
        [True, False, True, False, False],
        [False, False, True, False, False],
        [True, True, False, False, True]
    ]
    for set in dataset:
        msg = {
            "type":"parking",
            "data":set
        }
        payload = json.dumps(msg)
        client.publish("parking_ruiz", payload)
        time.sleep(10)


x2 = threading.Thread(target=manage_connection)
x2.start()

simulate_parking()