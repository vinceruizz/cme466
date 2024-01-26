import paho.mqtt.client as mqtt
import time
from random import randrange, uniform
import ntplib
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import math as m
import smbus
import RPi.GPIO as gpio
import time
import threading

i2c = smbus.SMBus(1)
swtPin = 13
ledPin = 19

gpio.setmode(gpio.BCM)
gpio.setup(swtPin, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(ledPin, gpio.OUT)

broker = "0.0.0.0"
client = mqtt.Client("client1")
client.connect(broker)

dbValue = 0

def getTime():
	ntpClient = ntplib.NTPClient()
	try:
		result = ntpClient.request("pool.ntp.org")
		time = result.tx_time
		print(f"Initial time: {time}")
		return time
	except Exception as e:
		print(f"Error with NTP. Got: {e}")

def encrypt(data, key):
	cipher = AES.new(key, AES.MODE_EAX)
	encryptedMessage = cipher.nonce + cipher.encrypt(pad(data.encode(), AES.block_size))
	return encryptedMessage

key = open("./key.bin", "rb").read()

def sound():
	while True:
		if gpio.input(swtPin) == 0:
			i2c.write_byte(0x48, 0x40) 
			i2c.read_byte(0x48)
			result = i2c.read_byte(0x48)
			#print(f"ADC Value: {result}")
			#wave(result)
			#print(result)
			dbValue = 20*(m.log(result/5, 10))

def light():
	flag = False
	while True:
		if gpio.input(swtPin) == 0:
			gpio.output(ledPin, gpio.HIGH)
			if flag == False:
				print("[PUBLISHER] The System is on!")
				flag = True
		else:
			gpio.output(ledPin, gpio.LOW)
			if flag == True:
				print("[PUBLISHER] The System is off!")
				flag = False

def publish():
	while True:
		print(f"DB Value: {dbValue}")
		initialTime = getTime()
		msg = {"data":dbValue,"timestamp":initialTime}
		payload = json.dumps(msg)
		encrypted_payload = encrypt(payload, key)
		client.publish("DB_LEVEL", encrypted_payload, qos=0, retain=True) # To change the QoS level, edit the >
		print("[PUBLISHER] Just published %s to topic \"DB_LEVEL\"" % json.loads(payload))
		time.sleep(1) 

x1 = threading.Thread(target=sound)
x2 = threading.Thread(target=light)
x3 = threading.Thread(target=publish)
x1.start()
x2.start()
x3.start()

 
