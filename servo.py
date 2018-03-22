import RPi.GPIO as GPIO
import time

class Servo:
    def __init__(self, pin, freq, start):
        global p
	GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)
        p = GPIO.PWM(pin, freq)
        p.start(((1.0/18.0)*start) + 2.5)
	p.ChangeDutyCycle(7.5)
        time.sleep(1)

    def move_servo(self, degree):
        global p
	dc = (((1.0/18.0)*degree) + 2.5)
        p.ChangeDutyCycle(dc)
        time.sleep(1)
	#print(dc)

    def cleanGPIO(self):
	 
	GPIO.cleanup()	

#p.ChangeDutyCycle(12.5) #180

#time.sleep(1)

#p.ChangeDutyCycle(2.5) #0

#time.sleep(1)
		
#p.ChangeDutyCycle(7.5) #90

#time.sleep(1)





	

	