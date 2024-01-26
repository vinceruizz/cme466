import paho.mqtt.client as mqtt
import json
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

key = open("./key.bin", "rb").read()

def on_message(client, userdata, message):
	encryptedData = message.payload
	try:
		received = json.loads(decrypt(encryptedData, key))
		data = received["data"]
		print("[SUBSCRIBER] Sensor dB level: %s dB" % str(data))
	except Exception as e:
		print(f"Decryption error. Got: {e}")

def decrypt(encryptedData, key):
	nonce = encryptedData[:16]
	ciphertext = encryptedData[16:]
	cipher = AES.new(key, AES.MODE_EAX, nonce)
	decryptedData = cipher.decrypt(ciphertext)
	return unpad(decryptedData, AES.block_size).decode()

broker = "0.0.0.0"
client = mqtt.Client("end_device")
client.connect(broker)

client.loop_start()
client.subscribe("DB_LEVEL") # you can change the QoS by adding parameter qos=x (replace x with desired QoS level (0, 1, 2)
client.on_message = on_message
time.sleep(30)
client.loop_end()
