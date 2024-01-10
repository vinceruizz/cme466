import PCF8591 as adc
import RPi.GPIO

GPIO.setmode(GPIO.BCM)

adc.setup(0x48)

count = 0
while True:
	val = adc.read(0)
	if val:
		print("Value: " + val)
		time.sleep(0.2)
