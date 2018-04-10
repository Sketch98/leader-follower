from math import pi

from drive_controller import DriveController
from parameters import angle_pid_constants, forward_pid_constants, \
    nav_timer_interval, small_angle, target_ball_dist
from pid import PID
from position import ZERO_POS
from repeated_timer import RepeatedTimer


class NavSystem:
    
    def __init__(self):
        self._drive_controller = DriveController()
        
        self._forward_pid = PID(forward_pid_constants)
        self._turn_pid = PID(angle_pid_constants)
        self._repeated_timer = RepeatedTimer(nav_timer_interval,
                                             self._timer_callback)
        
        self.pos_heading = (ZERO_POS, 0.0)
        self.dist_to_ball = target_ball_dist
        self.angle_to_ball = 0.0
        self.paused = False
        self.forward_velocity = 0.0
        self.angular_velocity = 0.0
    
    def steer_towards(self, rel_pos_from_ball_pov, ball_speed, ball_move_angle):
        pass
    
    def override_velocities(self, forward, angular):
        self.forward_velocity = forward
        self.angular_velocity = angular
    
    def calc_velocities(self, dist, angle, time_elapsed):
        if abs(angle) > pi/4:
            self.forward_velocity = self._forward_pid.calc(
                (dist - target_ball_dist)*0.1, time_elapsed)
            self.angular_velocity = self._turn_pid.calc(angle*4, time_elapsed)
        else:
            self.forward_velocity = self._forward_pid.calc(
                dist - target_ball_dist, time_elapsed)
            self.angular_velocity = self._turn_pid.calc(angle*0.5, time_elapsed)
    
    def update_angle_to_ball(self, angle):
        self.angle_to_ball = angle
    
    def dead_reckon_angle(self, turn_angle):
        self.angle_to_ball -= turn_angle
    
    def calc_velocities_2(self, time_elapsed):
        if abs(self.angle_to_ball) > pi/4:
            self.forward_velocity = self._forward_pid.calc(
                (self.dist_to_ball - target_ball_dist)*0.1, time_elapsed)
            self.angular_velocity = self._turn_pid.calc(self.angle_to_ball*4,
                                                        time_elapsed)
        else:
            self.forward_velocity = self._forward_pid.calc(
                self.dist_to_ball - target_ball_dist, time_elapsed)
            self.angular_velocity = self._turn_pid.calc(self.angle_to_ball*0.5,
                                                        time_elapsed)
    
    def _timer_callback(self, time_elapsed):
        # self._drive_controller.check_current()
        
        # calculate time since encoders were last read
        dist, angle = self._drive_controller.read_encoders(time_elapsed)
        
        # self.dead_reckon_angle(angle)
        # if lost ball slow to a stop
        if self.paused:
            self._drive_controller.update_motors(0.0, 0.0, time_elapsed)
            return
        self._dead_reckon(dist, angle)
        
        self._drive_controller.update_motors(self.forward_velocity,
                                             self.angular_velocity,
                                             time_elapsed)
    
    def _dead_reckon(self, dist, angle):
        if abs(angle) <= small_angle:
            pos = self.pos_heading[0].pos_from_dist_angle(dist, angle)
            theta = self.pos_heading[1] + angle%(2*pi)
            self.pos_heading = (pos, theta)
            return
        self._dead_reckon(dist/2, angle/2)
        self._dead_reckon(dist/2, angle/2)
    
    def start(self):
        self._repeated_timer.start()
    
    def stop(self):
        self._repeated_timer.stop()
        self._drive_controller.stop()
