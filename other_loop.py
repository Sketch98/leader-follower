from servo_controller import ServoController
from parameters import nav_timer_interval, servo_pin, servo_pid_constants, target_ball_dist
from repeated_timer import RepeatedTimer

class OtherLoop:
    def __init__(self):
        self.servo_controller = ServoController(servo_pin, servo_pid_constants)
        self.repeated_timer = RepeatedTimer(nav_timer_interval, self._timer_callback)
        
        self.dist_to_ball = target_ball_dist
        self.angle_to_ball = 0.0
    
    def _timer_callback(self, time_elapsed):
        pass
        # get dist and angle since last callback
        # adjust servo to account for robot's spin
        self.servo_controller.move_by(self.angle_to_ball)
        
        # calculate wanted forward and angular speed
    
    def update_angle_to_ball(self, angle):
        self.angle_to_ball = angle

    def dead_reckon_angle(self, turn_angle):
        self.angle_to_ball -= turn_angle
    
    def start(self):
        self.repeated_timer.start()
