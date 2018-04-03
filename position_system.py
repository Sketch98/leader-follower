from math import asin, tan

from filter import Filter
from parameters import camera_dist_offset, resolution, servo_pid_constants, servo_pin
from servo_controller import ServoController


def get_angle_to_pixel(x_pix):
    # corrects for camera's lens projecting curved light onto a flat sensor
    angle = asin(0.8643*(x_pix/resolution[0] - 0.5))
    return angle


def dist_angle_to_ball(x_pix, diameter):
    """
    finds the angles to the left and right sides of the ball.
    it uses that to estimate the distance and angle to the ball.
    """
    left_angle = get_angle_to_pixel(x_pix - diameter/2.0)
    right_angle = get_angle_to_pixel(x_pix + diameter/2.0)
    ball_angle = (right_angle + left_angle)/2
    dist = abs(33.1/tan((right_angle - left_angle))) + camera_dist_offset
    return dist, ball_angle


class PositionSystem:
    """
    finds the position of the ball relative to the vehicle
    """
    
    def __init__(self, raspi, nav_system):
        self._nav_system = nav_system
        self._servo_controller = ServoController(raspi, servo_pin, servo_pid_constants)
        self._dist_filter = Filter(coefficients=tuple([float(i + 1) for i in range(10)]))
        self._ball_filter = Filter(coefficients=tuple([float(i + 1) for i in range(10)]))
    
    def do_stuff(self, x, diameter):
        if x < 0:
            self._servo_controller.track()
            self._nav_system.paused = True
            return
        
        self._nav_system.paused = False
        dist, camera_to_ball_angle = dist_angle_to_ball(x, diameter)
        vehicle_to_ball_angle = camera_to_ball_angle + self._servo_controller.angle
        
        # move servo immediately
        self._servo_controller.move_by(camera_to_ball_angle)
        
        # filter dist and angle
        dist = self._dist_filter.queue(dist)
        vehicle_to_ball_angle = self._ball_filter.queue(vehicle_to_ball_angle)
        
        # tell nav system where ball is
        self._nav_system.dist_to_ball = dist
        self._nav_system.angle_to_ball = vehicle_to_ball_angle
        return
    
    def stop(self):
        self._servo_controller.stop()
