from math import cos, pi, sin

from drive_controller import DriveController
from parameters import angle_pid_constants, forward_pid_constants, nav_timer_interval, small_angle, target_dist_offset
from pid import PID
from time import sleep, time
from repeated_timer import RepeatedTimer


class NavSystem:
    
    def __init__(self):
        self._drive_controller = DriveController()
        self._forward_pid = PID(forward_pid_constants)
        self._turn_pid = PID(angle_pid_constants)
        self._timer = RepeatedTimer(nav_timer_interval, self._timer_callback)
        
        self.xy_theta = (0.0, 0.0, 0.0)
        self.dist_to_ball = target_dist_offset
        self.angle_to_ball = 0.0
        self.paused = False
        self.forward_velocity = 0.0
        self.angular_velocity = 0.0
        self._last_time = 0.0
    
    def calc_velocities(self, dist, angle):
        if abs(angle) > pi/4:
            self.forward_velocity = 0
            self.angular_velocity = self._turn_pid.calc(angle)*1.5
        else:
            self.forward_velocity = self._forward_pid.calc(dist - target_dist_offset)
            self.angular_velocity = self._turn_pid.calc(angle)
    
    def _timer_callback(self):
        self._drive_controller.check_current()
        
        # calculate time since encoders were last read
        interval = time() - self._last_time
        self._last_time = time()
        dist, angle = self._drive_controller.read_encoders(interval)
        
        # if lost ball slow to a stop
        if self.paused:
            self._drive_controller.update_motors(0.0, 0.0)
            return
        
        self._dead_reckon(dist, angle)
        
        self._drive_controller.update_motors(self.forward_velocity, self.angular_velocity)
    
    def _dead_reckon(self, dist, angle):
        if abs(angle) <= small_angle:
            x = self.xy_theta[0] + dist*sin(self.xy_theta[2])
            y = self.xy_theta[1] + dist*cos(self.xy_theta[2])
            theta = self.xy_theta[2] + angle%(2*pi)
            self.xy_theta = (x, y, theta)
            return
        self._dead_reckon(dist/2, angle/2)
        self._dead_reckon(dist/2, angle/2)
    
    def start(self):
        sleep(1)
        self._timer.start()
    
    def stop(self):
        self._timer.stop()
        self._drive_controller.stop()
