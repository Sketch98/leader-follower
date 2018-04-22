from math import pi

from globals import limit, symmetric_limit
from parameters import max_servo_move
from pid import PID
from servo import Servo
from timer import Timer


class ServoController:
    """Handles the high-level tasks of controlling a servo. It keeps track of
    the servo's angle and allows for relative movements."""
    def __init__(self, pin, pid_constants, left_limit=-pi*2/3, right_limit=pi/2):
        self._servo = Servo(pin)
        self._pid = PID(pid_constants)
        if left_limit >= right_limit:
            raise Exception('left_limit >= right_limit')
        self._left_limit = left_limit
        self._right_limit = right_limit
        self.angle = 0.0
        
        # servo cannot be set faster than 50Hz, so 20ms lower_limit
        self._timer = Timer(0.02)
    
    def move_by(self, offset):
        time_elapsed = self._timer.elapsed()
        if time_elapsed is None:
            return
        
        offset = self._pid.calc(offset, time_elapsed)
        
        # ensure that servo moves at most by max_move
        offset = symmetric_limit(offset, max_servo_move)
        self._move_to(self.angle + offset)
    
    def _move_to(self, angle):
        # ensure servo doesn't move beyond limits
        angle = limit(angle, self._left_limit, self._right_limit)
        self.angle = angle
        self._servo.move_to(self._angle_ratio(angle))
    
    def _angle_ratio(self, angle):
        return (angle - self._left_limit)/(self._right_limit - self._left_limit)
    
    def start(self):
        self._timer.start()
    
    def stop(self):
        self._move_to(0)
        self._pid.reset()
        self._timer.reset()


if __name__ == "__main__":
    from globals import raspi
    from time import sleep
    from parameters import servo_pid_constants
    
    servo_controller = ServoController(25, servo_pid_constants)
    sleep(1)
    servo_controller.move_by(-pi/2)
    sleep(0.1)
    for _ in range(100):
        servo_controller.move_by(-pi/2 - servo_controller.angle)
        sleep(0.01)
    servo_controller.move_by(pi/2 - servo_controller.angle)
    sleep(0.5)
    for _ in range(200):
        servo_controller.move_by(pi/2 - servo_controller.angle)
        sleep(0.01)
    
    servo_controller.stop()
    raspi.stop()
