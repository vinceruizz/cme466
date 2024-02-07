import math
import paho.mqtt.client as mqtt
import threading
import json
import time
import smbus
import RPi.GPIO as gpio

emergencyStatus = False

i2c = smbus.SMBus(1)
ledPin = 19

gpio.setmode(gpio.BCM)
gpio.setup(ledPin, gpio.OUT)

temp = 0

def on_message(client, userdata, message):
    global emergencyStatus
    try:
        payload = json.loads(message.payload)
        type = payload["type"]
        data = payload["data"]
        if type == "msg_board":
            print(f"[{type}] Received message: {str(data)}")
        if type == "emergency":
            if data:
                emergencyStatus = True
            else:
                emergencyStatus = False
            print(f"[{type}] Received message: {str(data)}")
    except Exception as e:
        print(f"Error processing message: {e}")

try:
    broker = "mqtt.eclipseprojects.io"
    client = mqtt.Client("msg_board_client_ruiz")
    client.connect(broker)
except Exception as e:
    print(f"Error connecting to broker: {e}")

def handleEmergency():
    global emergencyStatus

    while True:
        if emergencyStatus:
            gpio.output(ledPin, gpio.HIGH)
            time.sleep(0.25)
            gpio.output(ledPin, gpio.LOW)
            time.sleep(0.25)
        else:
            gpio.output(ledPin, gpio.LOW)

def readTemperature():
    global temp
    while True:
        i2c.write_byte(0x48, 0x40)
        i2c.read_byte(0x48)
        result = i2c.read_byte(0x48)

        Vr = 5 * float(result) / 255
        Rt = 10000 * Vr / (5 - Vr)
        temp = 1/(((math.log(Rt / 10000)) / 3950) + (1 / (273.15+25)))
        temp = temp - 273.15
        print ('temperature = ', temp, 'C')


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
        print(f"[msg_board] Just published {payload} to topic 'parking_ruiz;")
        time.sleep(5)

x1 = threading.Thread(target=simulate_parking)
x2 = threading.Thread(target=handleEmergency)
x3 = threading.Thread(target=readTemperature)
x1.start()
x2.start()

client.loop_start()
client.subscribe("MSG_BOARD") # you can change the QoS by adding parameter qos=x (replace x with desired QoS level (0, 1, 2)
client.subscribe("emergency")
client.on_message = on_message
time.sleep(100000)
client.loop_stop()