from servo import Servo


class ServoController:
    def __init__(self, pi, pin, left_limit=180, right_limit=0, start_angle=90, dead_zone=1, servo_speed=1.14, frame_rate=15, safety_factor=0.95):
        self.servo = Servo(pi, pin, left_limit, right_limit, start_angle)
        self.left_limit = left_limit
        self.right_limit = right_limit
        self.cur_angle = start_angle
        self.dead_zone = dead_zone
        self.last_seen = start_angle
        
        # the max angle that the servo can move by in 1 frame
        self.max_move = 360.0 * safety_factor / servo_speed / frame_rate
    
    def get_angle(self):
        return self.cur_angle
    
    def move_to_last_seen(self):
        self.move_by(-self.last_seen + self.cur_angle, seen=False)
    
    def limit(self, offset):
        # ensure servo doesn't move beyond limits
        angle_dest = self.cur_angle + offset
        if angle_dest > self.left_limit:
            angle_dest = self.left_limit
        elif angle_dest < self.right_limit:
            angle_dest = self.right_limit
        return angle_dest
    
    def move_by(self, offset, seen=True):
        # don't move inside dead_zone
        if abs(offset) < self.dead_zone:
            offset = 0
        
        if seen:
            self.last_seen = self.limit(offset)
        
        # ensure that servo moves at most by max_move
        if offset > self.max_move:
            offset = self.max_move
        elif offset < -self.max_move:
            offset = -self.max_move
        
        angle_dest = self.limit(offset)
        
        self.cur_angle = angle_dest
        self.servo.move_to(angle_dest)
    
    def stop(self):
        self.servo.off()
