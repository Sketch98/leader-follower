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
        self._pid = PID(pid_constants)
        
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
        
        # ensure servo doesn't move beyond limits
        angle_dst = limit(self.angle + offset, self._left_limit, self._right_limit)
        self.angle = angle_dst
        self._move_to(angle_dst)
    
    def _move_to(self, angle):
        self._servo.move_to((angle - self._left_limit)/(self._right_limit - self._left_limit))
    
    def stop(self):
        self.angle = (self._left_limit + self._right_limit)/2
        self._target = (self._left_limit + self._right_limit)/2
        self._pid.reset()
        self._servo.stop()


if __name__ == "__main__":
    import pigpio
    from time import sleep
    from parameters import servo_pid_constants
    
    raspi = pigpio.pi()
    servo_controller = ServoController(raspi, 25, servo_pid_constants)
    sleep(0.5)
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
