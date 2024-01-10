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

def sound():
	while True:
		i2c.write_byte(0x48, 0x40)
		i2c.read_byte(0x48)
		result = i2c.read_byte(0x48)
		print("value: " + str(result))
		time.sleep(0.5)
def light():
	while True:
		if gpio.input(swtPin) == 0:
			gpio.output(ledPin, gpio.HIGH)
		else:
			gpio.output(ledPin, gpio.LOW)

x1 = threading.Thread(target=sound)
x2 = threading.Thread(target=light)
x1.start()
x2.start()
	
