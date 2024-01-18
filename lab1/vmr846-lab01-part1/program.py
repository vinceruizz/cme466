import smbus
import RPi.GPIO as gpio
import time

i2c = smbus.SMBus(1)
swtPin = 13
ledPin = 19

gpio.setmode(gpio.BCM)
gpio.setup(swtPin, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(ledPin, gpio.OUT)

flag = False

while True:
	if gpio.input(swtPin) == 0:
		gpio.output(ledPin, gpio.HIGH)
		if flag == False:
			print("The System is on!")
			flag = True
	else:
		gpio.output(ledPin, gpio.LOW)
		if flag == True:
			print("The System is off!")
			flag = False
