import math

from filter import Filter
from mcp3008 import MCP3008
from motor_controller import MotorController
from repeated_timer import RepeatedTimer

wheel_diameter = 90.5  # 106.0
encoder_edges_per_rev = 192
# ratio of encoder edges to distance in mm
distance_coefficient = wheel_diameter * math.pi / encoder_edges_per_rev
distance_between_wheels = 450.0
max_edges_per_second = 16 * encoder_edges_per_rev


class DriveSystem:
    """
    controls the motors so that the robot navigates from one target to the next
    """
    
    def __init__(self, pi, left_pins, right_pins, motor_pid_constants, interval=0.01):
        self.pi = pi
        mcp = MCP3008()
        self.left_motor_controller = MotorController(pi, mcp, 0, left_pins, motor_pid_constants, forward=0)
        self.right_motor_controller = MotorController(pi, mcp, 1, right_pins, motor_pid_constants, forward=1)
        self.left_filter = Filter(coefficients=tuple([1.0] * 10))
        self.right_filter = Filter(coefficients=tuple([1.0] * 10))
        self.timer = RepeatedTimer(interval, self.timer_callback, i=interval)
        self.count = 0
        
        self.cur_x, self.cur_y, self.cur_theta = 0.0, 0.0, 0.0
        self.target_x, self.target_y, self.target_theta = 0.0, 0.0, 0.0
        self.grab = None
    
    def timer_callback(self, interval):
        # get movement of left and right wheels
        left_pos_dif = self.left_motor_controller.get_pos_dif() * distance_coefficient
        right_pos_dif = self.right_motor_controller.get_pos_dif() * distance_coefficient
        
        left_target_vel, right_target_vel = self.do_nav_stuff(left_pos_dif, right_pos_dif)
        
        # average 10 samples then calculate velocity
        left_pos_dif = self.left_filter.queue(left_pos_dif)
        right_pos_dif = self.right_filter.queue(right_pos_dif)
        left_vel = left_pos_dif / interval
        right_vel = right_pos_dif / interval
        
        self.left_motor_controller.adjust_motor_speed(left_target_vel, left_vel, max_edges_per_second)
        self.right_motor_controller.adjust_motor_speed(right_target_vel, right_vel, max_edges_per_second)
        
        self.count += 1
        if self.count >= 10:
            self.count = 0
            
            self.left_motor_controller.check_current()
            self.right_motor_controller.check_current()
    
    def dead_reckon(self, left_pos_dif, right_pos_dif):
        """
        estimates the movement of the robot based on the encoder movements
        """
        if left_pos_dif == right_pos_dif:
            if left_pos_dif != 0.0:
                self.cur_x += left_pos_dif * math.sin(self.cur_theta)
                self.cur_y += left_pos_dif * math.cos(self.cur_theta)
            return
        r3 = distance_between_wheels / 2
        if right_pos_dif != 0:
            r3 += distance_between_wheels / (left_pos_dif / right_pos_dif - 1)
        delta_theta = (
                              left_pos_dif - right_pos_dif) / 2.0 / \
                      math.pi / distance_between_wheels
        delta_x = r3 - math.cos(delta_theta)
        delta_y = math.sin(delta_theta)
        self.cur_x += delta_x * math.cos(self.cur_theta) + delta_y * math.sin(self.cur_theta)
        self.cur_y += delta_y * math.cos(self.cur_theta) - delta_y * math.sin(self.cur_theta)
        self.cur_theta += delta_theta
    
    def do_nav_stuff(self, left_pos_dif, right_pos_dif):
        # TODO: obviously
        print('IGNORE ME!')
        print(self.count)
        return -1000, 1000
    
    def set_grab(self, grab):
        self.grab = grab
    
    def grab_next_target(self):
        self.target_x, self.target_y = self.grab()
    
    def start(self):
        self.timer.start()
    
    def stop(self):
        self.timer.stop()
        self.left_motor_controller.stop()
        self.right_motor_controller.stop()


if __name__ == '__main__':
    import pigpio
    import time
    
    pi = pigpio.pi()
    left_pins = {'pwm': 6, 'dir': 5, 'a': 4, 'b': 17}
    right_pins = {'pwm': 26, 'dir': 13, 'a': 22, 'b': 27}
    motor_pid_constants = {'kp': 0.00102, 'ki': 0.0178333}
    d = DriveSystem(pi, left_pins, right_pins, motor_pid_constants)
    try:
        d.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        d.stop()
        pi.stop()
