import ball_estimator
from filter import Filter
from multiprocessing import Queue
from servo_controller import ServoController


class PositionSystem:
    def __init__(self, pi, servo_pin, drive_system, frame_rate=15, safety_factor=0.7):
        self.pi = pi
        self.servo_controller = ServoController(pi, servo_pin, frame_rate=frame_rate, safety_factor=safety_factor)
        self.drive_system = drive_system
        
        self.x_filter = Filter()
        # self.y_filter = Filter()
        self.diameter_filter = Filter()
        self.servo_queue = Queue(3)
        [self.servo_queue.put(90) for _ in range(3)]
        # self.x_pos_queue = Queue(100)
        # self.y_pos_queue = Queue(100)
    
    def adjust_servo(self, x, screenwidth):
        if x >= 0:
            angle = 26.75 * (x / screenwidth - 0.5)
            self.servo_controller.move_by(angle)
    
    def queue_camera_data(self, x, diameter, screenwidth):
        if x < 0:
            self.drive_system.stop()
            return
        
        self.x_filter.queue(x)
        # self.y_filter.queue(y)
        self.diameter_filter.queue(diameter)
        avg_x = self.x_filter.weighted_avg()
        # avg_y = self.y_filter.weighted_avg()
        avg_diameter = self.diameter_filter.weighted_avg()
        print(avg_diameter)
        
        servo_angle = self.servo_queue.get()
        self.servo_queue.put(self.servo_controller.get_angle())
        ball_angle = ball_estimator.get_ball_angle(servo_angle, x, screenwidth)
        
        self.drive_system.move(ball_angle, avg_diameter)
        # (x_pos, y_pos) = ball_estimator.calc_ball_coordinates(servo_angle, avg_x, screenwidth, avg_diameter)
        # if not self.x_pos_queue.full():
        #     self.x_pos_queue.put(x_pos)
        #     self.y_pos_queue.put(y_pos)
    
    # def next_target(self):
    #     return self.x_pos_queue.get(), self.y_pos_queue.get()
    #
    # def has_next_target(self):
    #     return not (self.x_pos_queue.empty() or self.x_pos_queue.empty())
