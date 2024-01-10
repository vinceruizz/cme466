import smbus
import RPi.GPIO as gpio
import time

i2c = smbus.SMBus(1)

while True:
	i2c.write_byte(0x48, 0x40)
	i2c.read_byte(0x48)
	result = i2c.read_byte(0x48)
	print("value: " + str(result))
	time.sleep(0.5)
