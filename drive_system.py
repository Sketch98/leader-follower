import math

from filter import Filter
from mcp3008 import MCP3008
from motor_controller import MotorController
from repeated_timer import RepeatedTimer
from pid import PIDController

wheel_diameter = 84.0  # 106.0
encoder_edges_per_rev = 192
# ratio of encoder edges to distance in mm
distance_coefficient = wheel_diameter * math.pi / encoder_edges_per_rev
distance_between_wheels = 400.0
max_edges_per_second = 16 * encoder_edges_per_rev


class DriveSystem:
    """
    controls the motors so that the robot navigates from one target to the next
    """
    
    def __init__(self, pi, left_pins, right_pins, motor_pid_constants, pos_pid_constants, interval=0.01):
        self.pi = pi
        mcp = MCP3008()
        self.left_motor_controller = MotorController(pi, mcp, 0, left_pins, motor_pid_constants, forward=0)
        self.right_motor_controller = MotorController(pi, mcp, 1, right_pins, motor_pid_constants, forward=1)
        self.left_filter = Filter(coefficients=tuple([1.0]*10))  # [float(i+1) for i in range(10)]
        self.right_filter = Filter(coefficients=tuple([1.0]*10))
        self.timer = RepeatedTimer(interval, self.timer_callback)
        self.count = 0
        
        self.cur_x, self.cur_y, self.cur_theta = 0.0, 0.0, 0.0
        self.target_x, self.target_y, self.target_theta = 0.0, 0.0, 0.0
        self.grab = None
        
        self.pos_pid = PIDController(pos_pid_constants['kp'], pos_pid_constants['ki'], pos_pid_constants['kd'])
    
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
        dist = (left_pos_dif + right_pos_dif) / 2
        angle = (left_pos_dif - right_pos_dif) / 2 / math.pi / distance_between_wheels
        self.transform_shit(dist, angle)
    
    def transform_shit(self, dist, angle, max_angle=math.pi/36):
        if abs(angle) <= max_angle:
            self.cur_theta += angle
            self.cur_x += dist * math.sin(self.cur_theta)
            self.cur_y += dist * math.cos(self.cur_theta)
            return
        self.transform_shit(dist/2, angle/2)
        self.transform_shit(dist/2, angle/2)
    
    def do_nav_stuff(self, left_pos_dif, right_pos_dif):
        # TODO: obviously
        self.dead_reckon(left_pos_dif, right_pos_dif)
        pid = self.pos_pid.calc(self.target_y - self.cur_y)
        print('pid = {:>4}  x = {:>4} y = {:>4} theta = {:>4}'
              .format(int(pid), int(self.cur_x), int(self.cur_y), int(self.cur_theta)))
        return pid, pid
    
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
    motor_pid_constants = {'kp': 0.00102, 'ki': 0.0178333, 'kd': 0}
    pos_pid_constants = {'kp': 1.2, 'ki': 0, 'kd': 0.1}
    d = DriveSystem(pi, left_pins, right_pins, motor_pid_constants, pos_pid_constants)
    try:
        d.start()
        time.sleep(1)
        d.target_y = 2000
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        d.stop()
        pi.stop()
