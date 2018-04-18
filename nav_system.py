from math import pi

from drive_controller import DriveController
from globals import correct_angle, symmetric_limit
from parameters import angle_pid_constants, forward_pid_constants, \
    max_angular_speed, max_forward_speed, nav_timer_interval, \
    servo_pid_constants, \
    servo_pin, target_ball_dist
from pid import PID
from position_system import PositionSystem
from repeated_timer import RepeatedTimer
from search_system import SearchSystem
from servo_controller import ServoController
from timer import Timer


class NavSystem:
    # TODO: implement updating distance and pos with dead reckoning
    # TODO: add searching when ball not seen
    def __init__(self):
        self._drive_controller = DriveController()
        self._search_system = SearchSystem()
        self._position_system = PositionSystem()
        self._camera_timer = Timer()
        self.servo_controller = ServoController(servo_pin, servo_pid_constants)
        self._repeated_timer = RepeatedTimer(nav_timer_interval,
                                             self._timer_callback)
        
        self._forward_pid = PID(forward_pid_constants)
        self._turn_pid = PID(angle_pid_constants)
        self._dist_to_ball = target_ball_dist
        self._abs_ball_angle = 0.0
        self._ball_speed = 0.0
        self._ball_heading = 0.0
        self._paused = False
        self._searching = False
    
    def _timer_callback(self, time_elapsed):
        if self._paused:
            self.reset()
            return
        
        # get dist and angle since last callback
        self._drive_controller.read_encoders(time_elapsed)
        self.adjust_servo()
        
        # calculate wanted forward and angular speed
        forward_vel, angular_vel = self.calc_velocities(time_elapsed)
        
        if self._searching:
            forward_vel = self._search_system.forward_speed(forward_vel)
            angular_vel = self._search_system.angular_speed(angular_vel)
        
        self._drive_controller.update_motors(forward_vel, angular_vel,
                                             time_elapsed)
    
    def adjust_servo(self):
        if self._searching:
            angle_error = self._search_system.servo(self.servo_controller.angle)
        else:
            # adjust servo to account for robot's spin
            angle_error = self._abs_ball_angle - self.abs_servo_angle()
            angle_error = correct_angle(angle_error)
        self.servo_controller.move_by(angle_error)
    
    def calc_velocities(self, time_elapsed):
        speed = self._drive_controller.robot_speed
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
        
        if abs(speed) > 1000:
            angle_error *= 0.1
        elif abs(speed) > 800:
            angle_error *= 0.2
        elif abs(speed) > 600:
            angle_error *= 0.3
        elif abs(speed) > 400:
            angle_error *= 0.6
        elif abs(speed) > 200:
            angle_error *= 0.8
        
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
    
    def update_ball_pos(self, dist, angle):
        if dist is None:
            self._searching = self._search_system.in_search_mode(None)
            self._ball_speed = 0
            self.slow_forward()
            return
        self._searching = False
        self._dist_to_ball = dist
        self._abs_ball_angle = correct_angle(self.abs_servo_angle() + angle)
        self._search_system.in_search_mode(self._abs_ball_angle)
    
    def pause(self):
        self._paused = True
    
    def resume(self):
        self._paused = False
    
    def start(self):
        self._camera_timer.start()
        self._repeated_timer.start()
        self.servo_controller.start()
    
    def stop(self):
        self._repeated_timer.stop()
        self._drive_controller.stop()
        self.servo_controller.stop()
        self._forward_pid.reset()
        self._turn_pid.reset()
    
    def reset(self):
        self._forward_pid.reset()
        self._turn_pid.reset()
        self._dist_to_ball = target_ball_dist
        self._abs_ball_angle = 0.0
        self._ball_speed = 0.0
        self._ball_heading = 0.0
        self.servo_controller.stop()
        self._drive_controller.reset()
        self._position_system.reset()
        self._search_system.reset()


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
