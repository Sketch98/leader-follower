from math import pi
from time import time

from servo_controller import ServoController
from parameters import nav_timer_interval, servo_pin, servo_pid_constants, target_ball_dist, forward_pid_constants, angle_pid_constants
from repeated_timer import RepeatedTimer
from drive_controller import DriveController
from pid import PID


class OtherLoop:
    def __init__(self):
        self.drive_controller = DriveController()
        self.servo_controller = ServoController(servo_pin, servo_pid_constants)
        self.repeated_timer = RepeatedTimer(nav_timer_interval, self._timer_callback)

        self.forward_pid = PID(forward_pid_constants)
        self.turn_pid = PID(angle_pid_constants)
        self.dist_to_ball = target_ball_dist
        self.abs_ball_angle = 0.0
        self.robot_angle = 0.0
        self.servo_time = 0.0
    
    def _timer_callback(self, time_elapsed):
        # get dist and angle since last callback
        dist, angle = self.drive_controller.read_encoders(time_elapsed)
        self.dead_reckon_angle(angle)
        # adjust servo to account for robot's spin
        dif = time() - self.servo_time
        if dif >= 0.02:
            self.servo_time += dif
            self.servo_controller.move_by(self.abs_ball_angle - self.abs_servo_angle(), time_elapsed)
        
        angle_to_ball = self.robot_angle - self.abs_ball_angle
        
        # calculate wanted forward and angular speed
        self.drive_controller.update_motors(*self.calc_velocities(dist, angle_to_ball), time_elapsed)
    
    def calc_velocities(self, dist, angle):
        if abs(angle) > pi/4:
            return self.forward_pid.calc((dist - target_ball_dist)*0.1), self.turn_pid.calc(angle*4)
        else:
            return self.forward_pid.calc(dist - target_ball_dist), self.turn_pid.calc(angle*0.5)
    
    def abs_servo_angle(self):
        return self.servo_controller.angle + self.robot_angle
    
    def update_ball_angle(self, angle):
        self.abs_ball_angle = self.abs_servo_angle() + angle
    
    def dead_reckon_angle(self, turn_angle):
        self.robot_angle += turn_angle
    
    def start(self):
        self.repeated_timer.start()
        self.servo_time = time()
