import paho.mqtt.client as mqtt
import time
import ntplib
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

key = open("./key.bin", "rb").read()

def on_message(client, userdata, message):
	encryptedData = message.payload
	try:
		received = json.loads(decrypt(encryptedData, key))
		data = received["data"]
		initialTime = received["timestamp"]
		print("[SUBSCRIBER] Received message: %s" % str(data))

		ntpClient = ntplib.NTPClient()
		try:
			currentTime = (ntpClient.request("pool.ntp.org")).tx_time
			latency = (currentTime - initialTime) * 1000
			print(f'[SUBSCRIBER] Transmission latency: {latency} ms')
		except Exception as e:
			print(f'Error with NTP. Got: {e}')
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
