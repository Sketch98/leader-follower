from globals import raspi
from nav_system import NavSystem
from position_system import PositionSystem
from search_system import SearchSystem
from timer import Timer
from vision import Vision


position_system = PositionSystem()
search_system = SearchSystem()
timer = Timer()
vision = Vision()
nav_system = NavSystem()

try:
    nav_system.start()
    timer.start()
    while True:
        dist, camera_to_ball_angle = vision.dist_angle_to_ball()
        time_elapsed = timer.elapsed()
        
        # search for ball
        # if search_system.in_search_mode(camera_to_ball_angle):
        #     a = search_system.search_servo(nav_system.servo_controller.angle)
        #     b = search_system.search_angular_speed()
        #     continue
        
        # if ball is seen move the servo to it and steer towards it
        if dist is None:
            print('no')
            nav_system.slow_forward()
        else:
            print('yes')
            nav_system.update_ball_pos(dist, camera_to_ball_angle)

except KeyboardInterrupt:
    pass
finally:
    nav_system.stop()
    vision.stop()
    raspi.stop()
