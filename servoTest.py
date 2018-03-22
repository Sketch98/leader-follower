import RPi.GPIO as GPIO
import time



GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
p = GPIO.PWM(11, 50)
p.start(7.5)
time.sleep(1)

p.ChangeDutyCycle(7.5)
time.sleep(1)

p.ChangeDutyCycle(12.5)
time.sleep(1)

p.ChangeDutyCycle(2.5)
time.sleep(1)
	 
GPIO.cleanup()	

#p.ChangeDutyCycle(12.5) #180

#time.sleep(1)

#p.ChangeDutyCycle(2.5) #0

#time.sleep(1)
		
#p.ChangeDutyCycle(7.5) #90

#time.sleep(1)





	

	