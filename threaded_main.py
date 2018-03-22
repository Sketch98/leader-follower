import vision
from servo_controller import ServoController
import pigpio
import time
from threading import Thread

pi = pigpio.pi()
servo_controller = ServoController(pi, 25, 180, 0, 90, dead_zone=2, safety_factor=0.8)
tracker = vision.MVision()
screenwidth = 640.0

try:
    last_time = time.time()
    times = [0.1, 0.0, 0.0, 0.0, 0.0]
    while True:
        tracker.grabframe()
        x = tracker.getX()
        if x >= 0:
            angle = 26.75 * (x / screenwidth - 0.5)
            print('x  = {}    angle = {}'.format(x, angle))
            servo_controller.move_by(angle)
        
        cur_time = time.time()
        times[4] = times[3]
        times[3] = times[2]
        times[2] = times[1]
        times[1] = times[0]
        times[0] = cur_time - last_time
        last_time = cur_time
        avg = 0.0
        for t in times:
            avg += t
        avg /= len(times)
        print(1.0 / avg)
except KeyboardInterrupt:
    pass
finally:
    servo_controller.off()
    tracker.closeVision()
