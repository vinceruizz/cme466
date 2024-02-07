import paho.mqtt.client as mqtt
import threading
import json
import time

def on_message(client, userdata, message):
    print("Received message")
    try:
        payload = json.loads(message.payload)
        type = payload["type"]
        data = payload["data"]
        print("Payload decoded")
        if type == "msg_board":
            print(f"[{type}] Received message: {str(data)}")
    except Exception as e:
        print(f"Error processing message: {e}")

try:
    broker = "mqtt.eclipseprojects.io"
    client = mqtt.Client("msg_board_client_ruiz")
    client.connect(broker)
    print("Connected to broker")
except Exception as e:
    print(f"Error connecting to broker: {e}")


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
        print(f"Just published {payload} to topic 'parking_ruiz;")
        time.sleep(5)

x1 = threading.Thread(target=simulate_parking)
x1.start()
# x2 = threading.Thread(target=manage_connection)
# x2.start()

client.loop_start()
client.subscribe("MSG_BOARD") # you can change the QoS by adding parameter qos=x (replace x with desired QoS level (0, 1, 2)
client.on_message = on_message
time.sleep(10000000)
client.loop_stop()