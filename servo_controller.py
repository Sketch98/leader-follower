from math import pi

from parameters import max_move
from pid import PID
from servo import Servo


def limit(val, lower_limit, upper_limit):
    # stops val from exceeding set limits
    return min(max(val, lower_limit), upper_limit)


class ServoController:
    def __init__(self, raspi, pin, pid_constants, left_limit=-pi/2, right_limit=pi/2):
        self._servo = Servo(raspi, pin)
        self._pid = PID(pid_constants['kp'], pid_constants['ki'], pid_constants['kd'])
        self._target = 0.0
        
        if right_limit >= left_limit:
            raise Exception('right_limit >= left_limit')
        self._left_limit = left_limit
        self._right_limit = right_limit
        self.angle = (self._left_limit + self._right_limit)/2
        self._target = self.angle
    
    def track(self):
        self.move_by(self._target - self.angle)
    
    def move_by(self, offset):
        # set target in case ball goes missing
        self._target = self.angle + offset
        
        offset = self._pid.calc(offset)
        
        # ensure that servo moves at most by max_move
        offset = limit(offset, -max_move, max_move)
        
        # ensure servo doesn't move beyond limits
        angle_dst = limit(self.angle + offset, self._left_limit, self._right_limit)
        self.angle = angle_dst
        self._move_to(angle_dst)
    
    def _move_to(self, angle):
        self._servo.move_to((angle - self._left_limit)/(self._right_limit - self._left_limit))
    
    def stop(self):
        self.angle = (self._left_limit + self._right_limit)/2
        self._target = (self._left_limit + self._right_limit)/2
        self._servo.stop()
        self._pid.reset()


if __name__ == "__main__":
    import pigpio
    import time
    
    raspi = pigpio.pi()
    pid_constants = {'kp': 0.25, 'ki': 0, 'kd': 0}
    servo_controller = ServoController(raspi, 18, pid_constants)
    time.sleep(1)
    for _ in range(18):
        servo_controller.move_by(-5)
        time.sleep(0.05)
    for _ in range(36):
        servo_controller.move_by(5)
        time.sleep(0.05)
    
    servo_controller.stop()
    raspi.stop()
