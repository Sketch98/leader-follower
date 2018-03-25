from multiprocessing import Queue

import ball_estimator
from servo_controller import ServoController


class PositionSystem:
    """
    finds the position of the ball relative to the vehicle
    """
    
    def __init__(self, pi, servo_pin, frame_rate):
        self.pi = pi
        self.servo_controller = ServoController(pi, servo_pin, frame_rate=frame_rate)
        self.x_pos_queue = Queue(100)
        self.y_pos_queue = Queue(100)
    
    def adjust_servo(self, ball_angle):
        self.servo_controller.move_by(ball_angle * 0.25)
    
    def find_ball_pos(self, x, diameter, screenwidth):
        if x < 0:
            # TODO: the servo should look for the ball in the case nothing is found
            # currently everything pauses when the ball isn't seen
            
            # self.drive_system.stop()
            return None
        
        servo_angle = self.servo_controller.get_angle()
        (x_pos, y_pos, ball_angle) = ball_estimator.calc_ball_coordinates(servo_angle, x, diameter, screenwidth)
        if not self.x_pos_queue.full():
            self.x_pos_queue.put(x_pos)
            self.y_pos_queue.put(y_pos)
        return ball_angle
    
    def next_target(self):
        return self.x_pos_queue.get(), self.y_pos_queue.get()
    
    def has_next_target(self):
        return not (self.x_pos_queue.empty() or self.y_pos_queue.empty())
