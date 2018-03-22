from threaded_vision import Vision
from servo_controller import ServoController
from motor import Motor
import pigpio
import time


pi = pigpio.pi()
right_motor = Motor(pi, 6, 5)
left_motor = Motor(pi, 26, 13)
servo_controller = ServoController(pi, 25, frame_rate=20)
screenwidth = 640.0
vision = Vision(int(screenwidth), 10)
vision.start()

try:
    last_time = time.time()
    while True:
        vision.grab_frame()
        x = vision.get_x()
        if x >= 0:
            angle = 26.75*(x/screenwidth-0.5)
            diameter = vision.get_diameter()
            # print('x  = {}     diameter={}     angle = {}'.format(x, diameter, angle))
            servo_controller.move_by(angle)
        else:
            # this is because the servo cant always move fast enough to catch up to the ball
            # while its still on the screen
            servo_controller.move_to_last_seen()
        
        cur_time = time.time()
        if cur_time != last_time:
            print(1.0/(cur_time - last_time))
        last_time = cur_time
except KeyboardInterrupt:
    pass
finally:
    left_motor.stop()
    right_motor.stop()
    servo_controller.stop()
    vision.stop()

