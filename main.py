from globals import raspi
from nav_system import NavSystem
from parameters import servo_pid_constants, servo_pin
from position_system import PositionSystem
from search_system import SearchSystem
from servo_controller import ServoController
from timer import Timer
from vision import Vision

nav_system = NavSystem()
position_system = PositionSystem()
search_system = SearchSystem()
servo_controller = ServoController(servo_pin, servo_pid_constants)
timer = Timer()
vision = Vision()

try:
    nav_system.start()
    timer.start()
    while True:
        dist, camera_to_ball_angle = vision.dist_angle_to_ball()
        time_elapsed = timer.elapsed()
        servo_angle = servo_controller.angle
        
        # search for ball
        if search_system.in_search_mode(camera_to_ball_angle):
            servo_controller.move_by(search_system.search_servo(servo_controller.angle))
            nav_system.override_velocities(0.0, search_system.search_motors())
            continue
        
        # if ball missing and not searching track servo and slow to a stop
        if camera_to_ball_angle is None:
            servo_controller.track()
            nav_system.override_velocities(0.0, 0.0)
            continue
        
        # if ball is seen move the servo to it and steer towards it
        servo_controller.move_by(camera_to_ball_angle)
        angle = camera_to_ball_angle + servo_angle
        
        # find the ball pos, heading, and speed
        # rel_ball_pos, ball_speed, ball_heading = position_system.calc_ball_movement(dist, angle, nav_system.xy_theta,
        #                                                                             time_elapsed)
        # nav_system.steer_towards(rel_ball_pos, ball_speed, ball_heading)
        
        nav_system.steer_towards(*position_system.calc_ball_movement(dist, angle, nav_system.pos_heading, time_elapsed))

except KeyboardInterrupt:
    pass
finally:
    nav_system.stop()
    servo_controller.stop()
    vision.stop()
    raspi.stop()
