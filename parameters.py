from math import pi

# pins
servo_pin = 25
left_pins = {'pwm': 6, 'dir': 5, 'a': 17, 'b': 27}
right_pins = {'pwm': 26, 'dir': 13, 'a': 23, 'b': 18}

# camera stuff
pink = ((160, 100, 120), (180, 210, 255))
resolution = (640, 480)
min_obj_radius = 5

# pids
servo_pid_constants = {'kp': 0.3, 'ki': 0, 'kd': 0.25}
motor_pid_constants = {'kp': 0.00102, 'ki': 0.0178333, 'kd': 0}
forward_pid_constants = {'kp': 1, 'ki': 0, 'kd': 0.2}
angle_pid_constants = {'kp': 1, 'ki': 0, 'kd': 0.2}

# encoder stuff
encoder_edges_per_rev = 192

# robot dimensions
# all distances in mm and angles in radians
wheel_radius = 50  # 42
wheel_circumference = wheel_radius*2*pi
distance_ratio = wheel_circumference/encoder_edges_per_rev
distance_between_wheels = 400.0
max_wheel_vel = 16*wheel_circumference

current_coefficient = 0.0488

camera_x_offset = 0
camera_y_offset = 0
camera_dist_offset = 0

servo_speed = 1.67
frame_rate = 10
max_move = 2*pi/servo_speed/frame_rate

motor_acceleration_limit = 1

target_dist_offset = 700
