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

# a sound visualizer representation of the sound sensor
def wave(val):
	if (val < 20):
		print("---")
	elif (val >= 20 and val < 40):
		print("-------")
	elif (val >= 40 and val < 60):
		print("-----------")
	elif (val >= 60 and val < 80):
		print("---------------")
	elif (val >= 80 and val < 100):
		print("-------------------")
	elif (val >= 100 and val < 120):
		print("-----------------------")
	elif (val >= 120 and val < 140):
		print("---------------------------")
	elif (val >= 140 and val < 160):
		print("-------------------------------")
	elif (val >= 160 and val < 180):
		print("-----------------------------------")
	elif (val >= 180 and val < 200):
		print("---------------------------------------")
	elif (val >= 200 and val < 220):
		print("-------------------------------------------")
	elif (val >= 220 and val < 240):
		print("-----------------------------------------------")
	else:
		print("---------------------------------------------------")
	time.sleep(0.05)

# prints the dB value of the sound visualizer using a 1V reference voltage (20 * log(adc value))
def db(value):
	result = 20*(m.log(value, 10))
	if result <= 40:
		print("It's pretty quiet around here. dB level: " + str(int(result)) + " dB")
	elif result <= 70:
		print("Getting noisier. Sounds like a busy office. dB level: " + str(int(result)) + " dB")
	elif result <= 100:
		print("It's loud in here! dB level: " + str(int(result)) + " dB")
	elif result <= 140:
		print("What, is My Bloody Valentine playing a concert?! dB level: " + str(int(result)) + " dB")
	else:
		print("TURN IT DOWN!!!!! dB level: " + str(int(result)) + " dB")
	time.sleep(0.5)
	
def sound():
	while True:
		if gpio.input(swtPin) == 0:
			i2c.write_byte(0x48, 0x40) 
			i2c.read_byte(0x48)
			result = i2c.read_byte(0x48)
			#wave(result)
			#print(result)
			db(result)

def light():
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

x1 = threading.Thread(target=sound)
x2 = threading.Thread(target=light)
x1.start()
x2.start()
	
