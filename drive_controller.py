from globals import correct_angle
from motor_controller import MotorController
from parameters import distance_between_wheels, left_motor_pid_constants, \
    left_pins, right_motor_pid_constants, right_pins, small_angle, robot_speed_smoothing_factors
from position import ZERO_POS
from filter import IrregularDoubleExponentialFilter


def forward_kin(left, right):
    forward = (left + right)/2
    angle = (left - right)/distance_between_wheels
    return forward, angle


def reverse_kin(forward, angle):
    left = forward + angle*distance_between_wheels/2
    right = forward - angle*distance_between_wheels/2
    return left, right


class DriveController:
    """
    Tracks the robot's position via dead reckoning and handles the motor's
    kinematics.
    
    The robot uses skid steering which has simple forward and reverse
    kinematics. DriveController is used to bridge the abstraction between a
    point model of the robot and the robot's actual layout."""
    
    def __init__(self):
        self._left_motor_controller = MotorController(0, left_pins,
                                                      left_motor_pid_constants,
                                                      0)
        self._right_motor_controller = MotorController(1, right_pins,
                                                       right_motor_pid_constants,
                                                       1)
        self._speed_filter = IrregularDoubleExponentialFilter(*robot_speed_smoothing_factors)
        
        self.pos_heading = (ZERO_POS, 0.0)
        self.robot_angle = 0.0
        self.robot_speed = 0.0
    
    def read_encoders(self, time_elapsed):
        """Reads the encoders and updates the robot's position, heading,
        and wheel velocities"""
        
        # get movement of left and right wheels
        left_dist_traveled = self._left_motor_controller.read_encoder(
            time_elapsed)
        right_dist_traveled = self._right_motor_controller.read_encoder(
            time_elapsed)
        dist, angle = forward_kin(left_dist_traveled, right_dist_traveled)
        # dead reckon pos and angle
        self.robot_angle = correct_angle(self.robot_angle + angle)
        # self.dead_reckon(dist, angle)
        
        self.robot_speed = self._speed_filter.filter(dist/time_elapsed, time_elapsed)
    
    def dead_reckon(self, dist, angle):
        """This method was tested in a previous version of the robot's software
        and it tracked the position of the robot very well when the tires didn't
        slip. Regrettably there wasn't enough time to integrate position system
        with the navigation system, so keeping track of the robot's position
        wouldn't yield any advantages.
        
        This method uses the point and shoot method. The point and shoot method
        estimates movement as a turn followed by a movement forward. Obviously
        the robot doesn't move like this but it is a good estimation when the
        total turn is small. If the turn is too large (>small_angle), then the
        movement is split into two consecutive point and shoots. This is done
        recursively while the angle is too large."""
        if abs(angle) <= small_angle:
            pos = self.pos_heading[0].pos_from_dist_angle(dist, angle)
            theta = correct_angle(self.pos_heading[1] + angle)
            self.pos_heading = (pos, theta)
            return
        self.dead_reckon(dist/2, angle/2)
        self.dead_reckon(dist/2, angle/2)
    
    def update_motors(self, forward_vel, angular_vel, time_elapsed):
        # Transform forward and angular to left and right and send to the
        # motor controllers
        left_target, right_target = reverse_kin(forward_vel, angular_vel)
        self._left_motor_controller.adjust_motor_speed(left_target,
                                                       time_elapsed)
        self._right_motor_controller.adjust_motor_speed(right_target,
                                                        time_elapsed)
    
    def check_current(self):
        # the current sensor don't work so this is never called in this version
        self._left_motor_controller.current_sensor.check_current()
        self._right_motor_controller.current_sensor.check_current()
    
    def reset(self):
        self._left_motor_controller.reset()
        self._right_motor_controller.reset()
        self.pos_heading = (ZERO_POS, 0.0)
        self.robot_angle = 0.0
        self.robot_speed = 0.0
    
    def stop(self):
        self._left_motor_controller.stop()
        self._right_motor_controller.stop()


if __name__ == '__main__':
    from globals import raspi
    from time import sleep
    
    d = DriveController()
    interval = 0.01
    try:
        while True:
            d.read_encoders(interval)
            d.update_motors(1000, 0.25, interval)
            sleep(interval)
    except KeyboardInterrupt:
        d.stop()
        raspi.stop()
