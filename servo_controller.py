from math import pi

from parameters import max_move, servo_dead_band
from pid import PID
from servo import Servo


def limit(val, lower_limit, upper_limit):
    # stops val from exceeding set limits
    return min(max(val, lower_limit), upper_limit)


class ServoController:
    def __init__(self, pin, pid_constants, left_limit=-pi/2, right_limit=pi/2):
        self._servo = Servo(pin)
        self._pid = PID(pid_constants, servo_dead_band)
        if left_limit >= right_limit:
            raise Exception('left_limit >= right_limit')
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
        self._move_to(self.angle + offset)
    
    def _move_to(self, angle):
        # ensure servo doesn't move beyond limits
        angle = limit(angle, self._left_limit, self._right_limit)
        self.angle = angle
        self._servo.move_to((angle - self._left_limit)/(self._right_limit - self._left_limit))
    
    def stop(self):
        self._move_to((self._left_limit + self._right_limit)/2)
        self._target = (self._left_limit + self._right_limit)/2
        self._pid.reset()
        self._servo.stop()


if __name__ == "__main__":
    from globals import raspi
    from time import sleep
    from parameters import servo_pid_constants
    
    servo_controller = ServoController(25, servo_pid_constants)
    sleep(1)
    servo_controller.move_by(-pi/2)
    sleep(0.1)
    for _ in range(10):
        servo_controller.track()
        sleep(0.1)
    servo_controller.move_by(pi)
    sleep(0.1)
    for _ in range(20):
        servo_controller.track()
        sleep(0.1)
    
    servo_controller.stop()
    raspi.stop()
