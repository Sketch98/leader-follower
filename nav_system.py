from math import pi
from time import time

from drive_controller import DriveController
from parameters import angle_pid_constants, forward_pid_constants, nav_timer_interval, small_angle, target_dist_offset
from pid import PID
from position import ZERO_POS
from repeated_timer import RepeatedTimer


class NavSystem:
    
    def __init__(self):
        self._drive_controller = DriveController()
        self._forward_pid = PID(forward_pid_constants)
        self._turn_pid = PID(angle_pid_constants)
        self._repeated_timer = RepeatedTimer(nav_timer_interval, self._timer_callback)
        
        self.pos_heading = (ZERO_POS, 0.0)
        self.dist_to_ball = target_dist_offset
        self.angle_to_ball = 0.0
        self.paused = False
        self.forward_velocity = 0.0
        self.angular_velocity = 0.0
        self._last_time = 0.0
    
    def steer_towards(self, rel_pos_from_ball_pov, ball_speed, ball_move_angle):
        pass
    
    def override_velocities(self, forward, angular):
        self.forward_velocity = forward
        self.angular_velocity = angular
    
    def calc_velocities(self, dist, angle):
        if abs(angle) > pi/4:
            self.forward_velocity = self._forward_pid.calc((dist - target_dist_offset)*0.1)
            self.angular_velocity = self._turn_pid.calc(angle*4)
        else:
            self.forward_velocity = self._forward_pid.calc(dist - target_dist_offset)
            self.angular_velocity = self._turn_pid.calc(angle*0.5)
    
    def _timer_callback(self):
        self._drive_controller.check_current()

        # calculate time since encoders were last read
        interval = time() - self._last_time
        self._last_time += interval
        dist, angle = self._drive_controller.read_encoders(interval)

        # if lost ball slow to a stop
        if self.paused:
            self._drive_controller.update_motors(0.0, 0.0)
            return
        # self._dead_reckon(dist, angle)
        
        self._drive_controller.update_motors(self.forward_velocity, self.angular_velocity)
    
    def _dead_reckon(self, dist, angle):
        if abs(angle) <= small_angle:
            pos = self.pos_heading[0].pos_from_dist_angle(dist, angle)
            theta = self.pos_heading[1] + angle%(2*pi)
            self.pos_heading = (pos, theta)
            return
        self._dead_reckon(dist/2, angle/2)
        self._dead_reckon(dist/2, angle/2)
    
    def start(self):
        self._last_time = time()
        self._repeated_timer.start()
    
    def stop(self):
        self._repeated_timer.stop()
        self._drive_controller.stop()
