import math
import paho.mqtt.client as mqtt
import threading
import json
import time
# import smbus
# import RPi.GPIO as gpio

# global emergency status and temperature variables
emergencyStatus = False
temp = 0

# # setup gpio
# i2c = smbus.SMBus(1)
# ledPin = 19
# gpio.setmode(gpio.BCM)
# gpio.setup(ledPin, gpio.OUT)

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

# depending on the emergencyStatus, either sets the led output to low (off), or blinks on and off
# def handleEmergency():
#     global emergencyStatus

#     while True:
#         if emergencyStatus:
#             gpio.output(ledPin, gpio.HIGH)
#             time.sleep(0.25)
#             gpio.output(ledPin, gpio.LOW)
#             time.sleep(0.25)
#         else:
#             gpio.output(ledPin, gpio.LOW)

# threaded loop that continuously reads values from the temperature sensor and updates the temperature variable
# def readTemperature():
#     global temp
#     while True:
#         i2c.write_byte(0x48, 0x40)
#         i2c.read_byte(0x48)
#         result = i2c.read_byte(0x48)

#         Vr = 5 * float(result) / 255
#         Rt = 10000 * Vr / (5 - Vr)
#         temp = 1/(((math.log(Rt / 10000)) / 3950) + (1 / (273.15+25)))
#         temp = temp - 273.15

# handler for publishing the converted temperature value
# def sendTemperature():
#     global temp

#     while True:
#         msg = {
#             "type":"temperature",
#             "data":temp
#         }
#         payload = json.dumps(msg)
#         client.publish("temperature_ruiz", payload)
#         print(f"[temperature] Just published {payload} to topic 'temperature;")
#         time.sleep(5)

# threaded parking simulation. Publishes a new set of parking data every 5 seconds
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

def simulate_image():
    dataset = [
        "https://bst.icons8.com/wp-content/uploads/2021/06/mona-lisa-low-quality.jpg",
        "https://i.ytimg.com/vi/IfrP8Z9q7Go/maxresdefault.jpg"
    ]
    for set in dataset:
        msg = {
            "type":"image",
            "data":set
        }
        payload = json.dumps(msg)
        client.publish("image_ruiz", payload)
        print(f"[msg_board] Just published {payload} to topic 'image_ruiz;")
        time.sleep(5)

def simulate_image_file():
    dataset = [
        "./test_images/"
    ]

# thread setup
# x1 = threading.Thread(target=simulate_parking)
# x2 = threading.Thread(target=handleEmergency)
# x3 = threading.Thread(target=readTemperature)
# x4 = threading.Thread(target=sendTemperature)
x5 = threading.Thread(target=simulate_image)
# x1.start()
# x2.start()
# x3.start()
# x4.start()
x5.start()

# mqtt client setup
client.loop_start()
client.subscribe("MSG_BOARD") # you can change the QoS by adding parameter qos=x (replace x with desired QoS level (0, 1, 2)
client.subscribe("emergency")
client.on_message = on_message
time.sleep(100000)
client.loop_stop()
