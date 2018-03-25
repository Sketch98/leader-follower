import math

from servo import Servo


def limit(val, lower_limit, upper_limit):
    # stops val from exceeding set limits
    if val < lower_limit:
        return lower_limit
    elif val > upper_limit:
        return upper_limit
    return val


class ServoController:
    """
    handles the non-hardware parts of controlling a servo which are relative movements
    and not allowing it to move beyond a certain distance per movement
    """
    
    def __init__(self, pi, pin, left_limit=-math.pi / 2, right_limit=math.pi / 2, start_angle=0, dead_zone=0,
                 servo_speed=1.14, frame_rate=35, safety_factor=0.95):
        self.servo = Servo(pi, pin, right_limit, left_limit, start_angle)
        self.left_limit = left_limit
        self.right_limit = right_limit
        self.cur_angle = start_angle
        self.dead_zone = dead_zone
        self.last_seen = start_angle
        
        # the max angle that the servo can move by in 1 frame
        self.max_move = 2 * math.pi * safety_factor / servo_speed / frame_rate
    
    def get_angle(self):
        return self.cur_angle
    
    def move_by(self, offset):
        # don't move inside dead_zone
        if abs(offset) < self.dead_zone:
            offset = 0
        
        # ensure that servo moves at most by max_move
        limit(offset, -self.max_move, self.max_move)
        
        # ensure servo doesn't move beyond limits
        angle_dst = limit(self.cur_angle + offset, self.left_limit, self.right_limit)
        
        self.cur_angle = angle_dst
        self.servo.move_to(angle_dst)
    
    def stop(self):
        self.servo.stop()
