from vision_controller import VisionController
from position_system import PositionSystem
# from drive_system import DriveSystem
import pigpio


# all distances in mm and angles in radians
pink = ((160, 100, 120), (180, 210, 255))
screenwidth = (320, 240)
frame_rate = 20
left_pins = {'pwm': 6, 'dir': 5, 'a': 0, 'b': 0}
right_pins = {'pwm': 26, 'dir': 13, 'a': 0, 'b': 0}
# TODO: tune this
motor_pid_constants = {'kp': 0.0, 'ki': 0.0, 'kd': 0.0}
pi = pigpio.pi()
v = VisionController(pink, screenwidth)
# d = DriveSystem(pi, left_pins, right_pins, motor_pid_constants)
p = PositionSystem(pi, 18, frame_rate)


def vision_callback(x, diameter, sw):
    ball_angle = p.find_ball_pos(x, diameter, sw)
    if ball_angle is not None:
        p.adjust_servo(ball_angle)


# def get_next_target():
#     if p.has_next_target():
#         p.next_target()


v.set_callback(vision_callback)

try:
    v.loop()
except KeyboardInterrupt:
    print('im dead')
finally:
    print('stopping')
    # d.stop()
