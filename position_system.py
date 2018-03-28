from math import asin, cos, sin, sqrt, tan
from multiprocessing import Queue
from time import time

from filter import Filter
from parameters import camera_x_offset, camera_y_offset, resolution, servo_pid_constants, servo_pin
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
    dist = abs(33.1/tan((right_angle - left_angle)))
    x = dist*sin(ball_angle)
    y = dist*cos(ball_angle)
    return x, y, dist, camera_to_ball_angle


def calc_abs_pos(x_vehicle, y_vehicle, vehicle_theta, x_ball, y_ball):
    x_ball += camera_x_offset
    y_ball += camera_y_offset
    x_abs = x_vehicle + x_ball*cos(vehicle_theta) - y_ball*sin(vehicle_theta)
    y_abs = y_vehicle - x_ball*sin(vehicle_theta) + y_ball*cos(vehicle_theta)
    return x_abs, y_abs


def calc_abs_pos2(x_vehicle, y_vehicle, theta, dist, angle):
    # does not account for camera offset
    x_abs = x_vehicle + dist*sin(theta + angle)
    y_abs = y_vehicle + dist*cos(theta + angle)
    return x_abs, y_abs


def calc_abs_dist(x0, y0, x1, y1):
    x_dif = x1 - x0
    y_dif = y1 - y0
    dist = sqrt(x_dif*x_dif + y_dif*y_dif)
    return dist


class PositionSystem:
    """
    finds the position of the ball relative to the vehicle
    """
    
    def __init__(self, raspi, nav_system):
        self._nav_system = nav_system
        self._servo_controller = ServoController(raspi, servo_pin, servo_pid_constants)
        self._servo_pid = PID(servo_pid_constants['kp'], servo_pid_constants['ki'], servo_pid_constants['kd'])
        self.dist_queue = Queue(100)
        self.speed_filter = Filter(coefficients=tuple([float(i + 1) for i in range(10)]))
        self.last_abs_x = None
        self.last_abs_y = None
        self.last_time = None
    
    def do_shit(self, x, diameter):
        if x < 0:
            self._servo_controller.track()
        
        servo_angle = self._servo_controller.angle
        (ball_x, ball_y, dist, ball_angle) = calc_ball_coordinates(servo_angle, x, diameter)
        self._servo_controller.move_by(self._servo_pid.calc(ball_angle))
        vehicle_x, vehicle_y, vehicle_theta = self._nav_system.x, self._nav_system.y, self._nav_system.theta
        x_abs, y_abs = calc_abs_pos(vehicle_x, vehicle_y, vehicle_theta, ball_x, ball_y)
        dist = 0
        speed = 0
        cur_time = time()
        if self.last_abs_x is not None:
            dist = calc_abs_dist(self.last_abs_x, self.last_abs_y, x_abs, y_abs)
            speed = dist/(cur_time - self.last_time)
        self.last_abs_x = x_abs
        self.last_abs_y = y_abs
        self.last_time = cur_time
        
        self._nav_system.dist_to_ball += dist
        self.dist_queue.put_nowait(dist)
        speed = self.speed_filter.queue(speed)
        
        return ball_angle
