import vision
import servo


CServo = servo.Servo(11,50,90)
tracker = vision.MVision()

#test=0

try:
    while True:
        tracker.grabframe()
	X = 480-tracker.getX()
	print((0.11146*X)+63.25)
	CServo.move_servo((0.11146*X)+63.25)
	#CServo.move_servo(test)
	#test = ((test+15) % (180))
except KeyboardInterrupt:

	tracker.closeVision()

	CServo.cleanGPIO()