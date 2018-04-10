from globals import raspi
from position_system import PositionSystem
from search_system import SearchSystem
from timer import Timer
from vision import Vision
from other_loop import OtherLoop

position_system = PositionSystem()
search_system = SearchSystem()
timer = Timer()
vision = Vision()
nav_system = OtherLoop()

try:
    nav_system.start()
    timer.start()
    while True:
        dist, camera_to_ball_angle = vision.dist_angle_to_ball()
        time_elapsed = timer.elapsed()
        
        # search for ball
        if search_system.in_search_mode(camera_to_ball_angle):
            a = search_system.search_servo(nav_system.servo_controller.angle)
            b = search_system.search_angular_speed()
            continue
        
        # if ball is seen move the servo to it and steer towards it
        if dist is not None:
            nav_system.update_ball_angle(camera_to_ball_angle)
        
        # find the ball pos, heading, and speed
        # rel_ball_pos, ball_speed, ball_heading = position_system.calc_ball_movement(dist, angle, nav_system.xy_theta,
        #                                                                             time_elapsed)

except KeyboardInterrupt:
    pass
finally:
    # timer.close()
    vision.stop()
    raspi.stop()
