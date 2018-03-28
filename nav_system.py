from math import cos, pi, sin

from drive_controller import DriveController
from parameters import speed_pid_constants
from pid import PID
from repeated_timer import RepeatedTimer
from parameters import target_dist_offset


class NavSystem:
    """
    nav's shit
    """
    
    def __init__(self, raspi, interval=0.01):
        self._drive_controller = DriveController(raspi)
        self._speed_pid = PID(speed_pid_constants['kp'], speed_pid_constants['ki'], speed_pid_constants['kd'])
        self.x, self.y, self.theta = 0.0, 0.0, 0.0
        self._timer = RepeatedTimer(interval, self.timer_callback)
        self.dist_to_ball = 0.0
    
    def timer_callback(self, interval):
        self._drive_controller.check_current()
        dist, angle = self._drive_controller.read_encoders(interval)
        self.dead_reckon(dist, angle)
        
        forward_velocity = self._speed_pid.calc(dist - target_dist_offset)
        # TODO figure out angular velocity
        angular_velocity = 0
        self._drive_controller.update_motors(forward_velocity, angular_velocity)
    
    def dead_reckon(self, dist, angle, max_angle=pi/36):
        if abs(angle) <= max_angle:
            self.theta += angle % (2*pi)
            self.x += dist*sin(self.theta)
            self.y += dist*cos(self.theta)
            return
        self.dead_reckon(dist/2, angle/2)
        self.dead_reckon(dist/2, angle/2)
    
    def do_nav_stuff(self, dist, angle):
        # TODO: obviously
        pass
    
    def start(self):
        self._timer.start()
    
    def stop(self):
        self._timer.stop()
        self._drive_controller.stop()


if __name__ == '__main__':
    import pigpio
    import time
    
    raspi = pigpio.pi()
    n = NavSystem(raspi)
    try:
        n.start()
        time.sleep(1)
        n.target_y = 2000
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        n.stop()
        raspi.stop()