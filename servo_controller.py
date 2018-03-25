import math

from servo import Servo


def limit(val, lower_limit, upper_limit):
    # stops val from exceeding set limits
    if val < lower_limit:
        return lower_limit
    elif val > upper_limit:
        return upper_limit
    return val


servo_speed = 1.14
frame_rate = 35
max_move = 2 * math.pi / servo_speed / frame_rate


class ServoController:
    """
    handles the non-gpio parts of controlling a servo which are relative
    movements and not allowing it to move beyond a certain distance per movement
    """
    
    def __init__(self, pi, pin, left_limit=-math.pi / 2, right_limit=math.pi / 2):
        self.servo = Servo(pi, pin, right_limit, left_limit)
        self.left_limit = left_limit
        self.right_limit = right_limit
        self.cur_angle = (left_limit + right_limit) / 2
    
    def get_angle(self):
        return self.cur_angle
    
    def move_by(self, offset):
        # ensure that servo moves at most by max_move
        limit(offset, -max_move, max_move)
        
        # ensure servo doesn't move beyond limits
        angle_dst = limit(self.cur_angle + offset, self.left_limit,
                          self.right_limit)
        
        self.cur_angle = angle_dst
        self.servo.move_to(angle_dst)
    
    def stop(self):
        self.servo.stop()
