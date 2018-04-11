from math import pi

from drive_controller import DriveController
from globals import symmetric_limit, correct_angle
from parameters import angle_pid_constants, forward_pid_constants, \
    max_angular_speed, max_forward_speed, nav_timer_interval, servo_pid_constants, \
    servo_pin, target_ball_dist
from pid import PID
from repeated_timer import RepeatedTimer
from servo_controller import ServoController


class NavSystem:
    # TODO: implement updating distance and pos with dead reckoning
    def __init__(self):
        self._drive_controller = DriveController()
        self.servo_controller = ServoController(servo_pin, servo_pid_constants)
        self._repeated_timer = RepeatedTimer(nav_timer_interval,
                                             self._timer_callback)
        
        self._forward_pid = PID(forward_pid_constants)
        self._turn_pid = PID(angle_pid_constants)
        self._dist_to_ball = target_ball_dist
        self._abs_ball_angle = 0.0
    
    def _timer_callback(self, time_elapsed):
        # get dist and angle since last callback
        dist = self._drive_controller.read_encoders(time_elapsed)
        
        # adjust servo to account for robot's spin
        angle_error = self._abs_ball_angle - self.abs_servo_angle()
        angle_error = correct_angle(angle_error)
        self.servo_controller.move_by(angle_error)
        
        # calculate wanted forward and angular speed
        forward_vel, angular_vel = self.calc_velocities(time_elapsed)
        self._drive_controller.update_motors(forward_vel, angular_vel,
                                             time_elapsed)
    
    def calc_velocities(self, time_elapsed):
        dist_error = self._dist_to_ball - target_ball_dist
        angle_error = self._abs_ball_angle - self._drive_controller.robot_angle
        angle_error = correct_angle(angle_error)
        if abs(angle_error) > pi*5/12:
            dist_error *= 0
        elif abs(angle_error) > pi/3:
            dist_error *= 0.15
        elif abs(angle_error) > pi/4:
            dist_error *= 0.3
        elif abs(angle_error) > pi/6:
            dist_error *= 0.5
        elif abs(angle_error) > pi/12:
            dist_error *= 0.9
        
        print(dist_error)
        
        forward_vel = self._forward_pid.calc(dist_error, time_elapsed)
        angular_vel = self._turn_pid.calc(angle_error, time_elapsed)
        forward_vel = symmetric_limit(forward_vel, max_forward_speed)
        angular_vel = symmetric_limit(angular_vel, max_angular_speed)
        return forward_vel, angular_vel
    
    def abs_servo_angle(self):
        a = self.servo_controller.angle + self._drive_controller.robot_angle
        return correct_angle(a)
    
    def slow_forward(self):
        self._dist_to_ball = target_ball_dist
        self._forward_pid.reset()
    
    def update_ball_pos(self, dist, angle):
        self._dist_to_ball = dist
        self._abs_ball_angle = correct_angle(self.abs_servo_angle() + angle)
    
    def start(self):
        self._repeated_timer.start()
        self.servo_controller.start()
    
    def stop(self):
        self._repeated_timer.stop()
        self._drive_controller.stop()
        self.servo_controller.stop()
        self._forward_pid.reset()
        self._turn_pid.reset()


if __name__ == '__main__':
    from time import sleep
    from globals import raspi
    
    nav_system = NavSystem()
    try:
        nav_system.start()
        while True:
            sleep(10)
    except KeyboardInterrupt:
        pass
    finally:
        nav_system.stop()
        raspi.stop()
