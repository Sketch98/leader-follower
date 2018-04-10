from filter import DoubleExponentialFilter
from motor_controller import MotorController
from parameters import distance_between_wheels, distance_ratio, left_pins, left_motor_pid_constants, \
    right_motor_pid_constants, right_pins, smoothing_factor, trend_smoothing_factor


class DriveController:
    """
    implement forward and reverse kinematics of the robot's motors
    """
    
    def __init__(self):
        self._left_motor_controller = MotorController(0, left_pins, left_motor_pid_constants, 0)
        self._right_motor_controller = MotorController(1, right_pins, right_motor_pid_constants, 1)
        self._left_filter = DoubleExponentialFilter(smoothing_factor, trend_smoothing_factor)
        self._right_filter = DoubleExponentialFilter(smoothing_factor, trend_smoothing_factor)
        self._left_vel = 0
        self._right_vel = 0
    
    def read_encoders(self, interval):
        # get movement of left and right wheels
        left_pos_dif = self._left_motor_controller.get_pos_dif()*distance_ratio
        right_pos_dif = self._right_motor_controller.get_pos_dif()*distance_ratio
        
        # average 10 samples and update wheel velocities
        left_pos_dif = self._left_filter.filter(left_pos_dif)
        right_pos_dif = self._right_filter.filter(right_pos_dif)
        self._left_vel = left_pos_dif/interval
        self._right_vel = right_pos_dif/interval
        
        # use point and shoot method to estimate distance and angle
        dist = (left_pos_dif + right_pos_dif)/2
        angle = (left_pos_dif - right_pos_dif)/distance_between_wheels
        return dist, angle
    
    def update_motors(self, forward_vel, angular_vel, time_elapsed):
        target_left_vel = forward_vel + distance_between_wheels*angular_vel/2
        target_right_vel = forward_vel - distance_between_wheels*angular_vel/2
        self._left_motor_controller.adjust_motor_speed(target_left_vel, self._left_vel, time_elapsed)
        self._right_motor_controller.adjust_motor_speed(target_right_vel, self._right_vel, time_elapsed)
    
    def check_current(self):
        self._left_motor_controller.check_current()
        self._right_motor_controller.check_current()
    
    def stop(self):
        self._left_motor_controller.stop()
        self._right_motor_controller.stop()


if __name__ == '__main__':
    from globals import raspi
    from time import sleep
    
    d = DriveController()
    try:
        while True:
            d.read_encoders(0.01)
            d.update_motors(1000, 0.25, 0.01)
            sleep(0.01)
    except KeyboardInterrupt:
        d.stop()
        raspi.stop()
