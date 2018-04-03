from math import cos, pi, sin

from drive_controller import DriveController
from parameters import target_dist_offset, forward_pid_constants, angle_pid_constants, small_angle, nav_timer_interval
from pid import PID
from repeated_timer import RepeatedTimer


class NavSystem:
    """
    nav's shit
    """
    
    def __init__(self, raspi):
        self._drive_controller = DriveController(raspi)
        self._forward_pid = PID(forward_pid_constants)
        self._turn_pid = PID(angle_pid_constants)
        self._timer = RepeatedTimer(nav_timer_interval, self.timer_callback)
        
        self.xy_theta = (0.0, 0.0, 0.0)
        self.dist_to_ball = target_dist_offset
        self.angle_to_ball = 0.0
        self.paused = False
    
    def timer_callback(self, interval):
        self._drive_controller.check_current()
        
        dist, angle = self._drive_controller.read_encoders(interval)
        if self.paused:
            self._drive_controller.update_motors(0.0, 0.0)
            return
        
        # self.dead_reckon(dist, angle)
        
        forward_velocity = self._forward_pid.calc(self.dist_to_ball - target_dist_offset)
        angular_velocity = self._turn_pid.calc(self.angle_to_ball)
        self._drive_controller.update_motors(forward_velocity, angular_velocity)
    
    def dead_reckon(self, dist, angle):
        if abs(angle) <= small_angle:
            x = self.xy_theta[0] + dist*sin(self.xy_theta[2])
            y = self.xy_theta[1] + dist*cos(self.xy_theta[2])
            theta = self.xy_theta[2] + angle%(2*pi)
            self.xy_theta = (x, y, theta)
            return
        self.dead_reckon(dist/2, angle/2)
        self.dead_reckon(dist/2, angle/2)
    
    def start(self):
        self._timer.start()
    
    def stop(self):
        self._timer.stop()
        self._drive_controller.stop()
