from globals import raspi
from nav_system import NavSystem
from vision import Vision
# from position_system import PositionSystem
# from timer import Timer


# position_system = PositionSystem()
# timer = Timer()
vision = Vision()
nav_system = NavSystem()
try:
    nav_system.start()
    # timer.start()
    while True:
        dist, camera_to_ball_angle = vision.dist_angle_to_ball()
        # time_elapsed = timer.elapsed()
        nav_system.update_ball_pos(dist, camera_to_ball_angle)

except KeyboardInterrupt:
    pass
finally:
    nav_system.stop()
    vision.stop()
    raspi.stop()
