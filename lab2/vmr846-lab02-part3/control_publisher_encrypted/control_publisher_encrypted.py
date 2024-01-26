import paho.mqtt.client as mqtt
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import math as m
import smbus
import RPi.GPIO as gpio
import time
import threading

broker = "0.0.0.0"
client = mqtt.Client("client2")
client.connect(broker)

def encrypt(data, key):
	cipher = AES.new(key, AES.MODE_EAX)
	encryptedMessage = cipher.nonce + cipher.encrypt(pad(data.encode(), AES.block_size))
	return encryptedMessage

key = open("./key.bin", "rb").read()


while True:
	flag = True
	controlInput = 'n'
	while flag:
		controlInput = input("Turn lights on or off? Type on/off: ")
		if controlInput == 'off' or controlInput == 'on':
			flag = False
		else:
			print("Invalid input")
	msg = {"data":controlInput}
	payload = json.dumps(msg)
	encrypted_payload = encrypt(payload, key)
	client.publish("light", encrypted_payload, qos=0, retain=True) # To change the QoS level, edit the >
	print("[PUBLISHER] Just published %s to topic \"light\"" % json.loads(payload))
	time.sleep(0.25) 
