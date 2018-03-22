from motor_controller import MotorController
from mcp3008 import MCP3008
from threading import Timer
import math


# ratio of encoder edges to distance in mm
wheel_diameter = 106.0
encoder_edges_per_rev = 192
distance_coefficient = wheel_diameter*math.pi/encoder_edges_per_rev
distance_between_wheels = 450.0


class DriveSystem:
    """
    controls the motors so that the robot navigates from one target to the next
    """
    def __init__(self, pi, left_pins, right_pins, motor_pid_constants, interval=0.01):
        self.pi = pi
        mcp = MCP3008()
        left_channel = 0
        right_channel = 1
        self.left_motor_controller = \
            MotorController(pi, mcp, left_channel, left_pins, motor_pid_constants, forward=1, interval=interval)
        self.right_motor_controller = \
            MotorController(pi, mcp, right_channel, right_pins, motor_pid_constants, forward=1, interval=interval)
        self.timer = Timer(interval, self.timer_callback)
        self.count = 0
        self.interval = interval
        
        self.cur_x = 0.0
        self.cur_y = 0.0
        self.cur_theta = 0.0
        self.target_x = 0.0
        self.target_y = 0.0
        # self.target_theta = 0.0
        self.grab = None
    
    def start(self):
        self.timer.start()
    
    def stop(self):
        self.left_motor_controller.stop()
        self.right_motor_controller.stop()
        self.timer.cancel()
    
    def set_grab(self, grab):
        self.grab = grab
    
    def timer_callback(self):
        left_pos_dif = self.left_motor_controller.get_pos_dif() * distance_coefficient
        right_pos_dif = self.right_motor_controller.get_pos_dif() * distance_coefficient
        left_target_vel, right_target_vel = self.do_nav_shit(left_pos_dif, right_pos_dif)
        left_vel = left_pos_dif/self.interval
        right_vel = right_pos_dif/self.interval
        self.left_motor_controller.do_mo_shit(left_target_vel, left_vel)
        self.right_motor_controller.do_mo_shit(left_target_vel, right_vel)
        self.count += 1
        if self.count >= 10:
            self.count = 0
            # TODO: the motor should temporarily stop while the current lowers instead of shutting off permanently
            if self.left_motor_controller.check_current():
                self.left_motor_controller.stop()
                raise Exception('left motor current trip')
            if self.right_motor_controller.check_current():
                self.right_motor_controller.stop()
                raise Exception('right motor current trip')
    
    def dead_reckon(self, left_pos_dif, right_pos_dif):
        """
        estimates the movement of the robot based on the encoder movements
        """
        if left_pos_dif == right_pos_dif:
            if left_pos_dif != 0.0:
                self.cur_x += left_pos_dif * math.sin(self.theta)
                self.cur_y += left_pos_dif * math.cos(self.theta)
            return
        r3 = distance_between_wheels/2
        if right_pos_dif != 0:
            r3 += distance_between_wheels/(left_pos_dif/right_pos_dif - 1)
        theta = (left_pos_dif - right_pos_dif)/2.0/math.pi/distance_between_wheels
        delta_x = r3 - math.cos(theta)
        delta_y = math.sin(theta)
        self.cur_x += delta_x*math.cos(self.theta) + delta_y*math.sin(self.theta)
        self.cur_y += delta_y*math.cos(self.theta) - delta_y*math.sin(self.theta)
        self.cur_theta += theta
    
    def do_nav_stuff(self, left_pos_dif, right_pos_dif):
        # TODO: obviously
        print('IGNORE ME!')
        print(self.count)
        return 0.0, 0.0
    
    def grab_next_target(self):
        self.target_x, self.target_y = self.grab()
