from math import asin, cos, sin, sqrt, tan

from filter import Filter
from parameters import camera_x_offset, camera_y_offset, camera_dist_offset, resolution, servo_pid_constants, servo_pin
from pid import PID
from servo_controller import ServoController


def get_angle_to_pixel(x_pix):
    # corrects for camera's lens projecting curved light onto a flat sensor
    angle = asin(0.8643*(x_pix/resolution[0] - 0.5))
    return angle


def calc_ball_coordinates(servo_angle, x_pix, diameter):
    """
    finds the angles to the left and right sides of the ball.
    it uses that to estimate the distance to the ball and the ball's relative
    xy position
    """
    left_angle = get_angle_to_pixel(x_pix - diameter/2.0)
    right_angle = get_angle_to_pixel(x_pix + diameter/2.0)
    camera_to_ball_angle = (right_angle + left_angle)/2
    ball_angle = servo_angle + camera_to_ball_angle
    dist = abs(33.1/tan((right_angle - left_angle))) + camera_dist_offset
    x = dist*sin(ball_angle)
    y = dist*cos(ball_angle)
    return x, y, dist, camera_to_ball_angle


def calc_abs_pos(x_vehicle, y_vehicle, vehicle_theta, x_ball, y_ball):
    x_ball += camera_x_offset
    y_ball += camera_y_offset
    x_abs = x_vehicle + x_ball*cos(vehicle_theta) - y_ball*sin(vehicle_theta)
    y_abs = y_vehicle - x_ball*sin(vehicle_theta) + y_ball*cos(vehicle_theta)
    return x_abs, y_abs


class PositionSystem:
    """
    finds the position of the ball relative to the vehicle
    """
    
    def __init__(self, raspi, nav_system):
        self._nav_system = nav_system
        self._servo_controller = ServoController(raspi, servo_pin, servo_pid_constants)
        self._servo_pid = PID(servo_pid_constants['kp'], servo_pid_constants['ki'], servo_pid_constants['kd'])
        self.dist_filter = Filter(coefficients=tuple([float(i + 1) for i in range(10)]))
    
    def do_shit(self, x, diameter):
        if x < 0:
            self._servo_controller.track()
        
        servo_angle = self._servo_controller.angle
        (ball_x, ball_y, dist, ball_angle) = calc_ball_coordinates(servo_angle, x, diameter)
        self._servo_controller.move_by(self._servo_pid.calc(ball_angle))
        self._nav_system.dist_to_ball = self.dist_filter.queue(dist)
        self._nav_system.angle_to_ball = ball_angle
        
        return ball_angle
