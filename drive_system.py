from motor import Motor
# from rotary_encoder import RotaryEncoder
from threading import Thread
import time


class DriveSystem:
    def __init__(self, pi, right_pwm, right_dir, left_pwm, left_dir):
        self.pi = pi
        self.right_motor = Motor(pi, right_pwm, right_dir, forward=1)
        self.left_motor = Motor(pi, left_pwm, left_dir, forward=0)
        # self.left_encoder = RotaryEncoder(pi, left_a, left_b, left_x)
        # self.right_encoder = RotaryEncoder(pi, right_a, right_b, right_x)
        # self.get_next_target = get_next_target
        # self.callback = None
        # self.stopped = False
    
    def move(self, angle, diameter):
        speed = 0
        if diameter < 50:
            speed = 0.3
        elif diameter < 120:
            speed = 0.2
        
        turn_speed = (angle - 90)/90/15
        right_speed = min(0.25, max(-0.25, speed-turn_speed))
        left_speed = min(0.25, max(-0.25, (speed+turn_speed)))
        # print('right_speed {}   left_speed {}'.format(right_speed,left_speed))
        self.left_motor.set_speed(left_speed)
        self.right_motor.set_speed(right_speed)

    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()
    
    # def set_callback(self, callback):
    #     self.callback = callback
    
    # def start(self):
    #     th = Thread(target=self.loop, args=())
    #     th.daemon = True
    #     th.start()
    #
    # def stop(self):
    #     self.stopped = True
    #     self.left_motor.stop()
    #     self.right_motor.stop()
    
    # def loop(self):
    #     # assert self.callback is not None, 'must have callback function before starting vision loop'
    #     angle = 90
    #     diameter = 50
    #     while not self.stopped:
    #         if diameter < 25:
    #             self.left_motor.set_speed(0.2)
    #         if diameter < 50:
    #             self.left_motor.set_speed(0.15)
    #         # self.left_motor.set_speed(0.15)
    #         # self.right_motor.set_speed(-0.115)
    #         time.sleep(1)
