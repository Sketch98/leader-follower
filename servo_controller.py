from servo import Servo

class ServoController:
    def __init__(self, pi, pin, left_limit, right_limit, start_angle, dead_zone=1, servo_speed=1.14, frame_rate=15, safety_factor=0.95):
        self.servo = Servo(pi, pin, left_limit, right_limit, start_angle)
        self.left_limit = left_limit
        self.right_limit = right_limit
        self.cur_angle = start_angle
        self.dead_zone = dead_zone
        
        # the max angle that the servo can move by in 1 frame
        self.max_move = 360.0*safety_factor/servo_speed/frame_rate
     
    def move_by(self, angle):
        # don't move inside dead_zone
        if abs(angle) < self.dead_zone:
            angle = 0
        
        # ensure that servo moves at most by max_move
        if angle > self.max_move:
            angle = self.max_move
        elif angle < -self.max_move:
            angle = -self.max_move
            
        # ensure servo doesn't move beyond limits
        angle_dest = self.cur_angle + angle
        if angle_dest > self.left_limit:
            angle_dest = self.left_limit
            angle = self.left_limit - self.cur_angle
        elif angle_dest < self.right_limit:
            angle_dest = self.right_limit
            angle = self.right_limit - self.cur_angle
        
        self.cur_angle = angle_dest
        self.servo.move_to(angle_dest)
     
    def off(self):
        self.servo.off()
