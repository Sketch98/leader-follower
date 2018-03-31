from math import pi

# pins
servo_pin = 18
left_pins = {'pwm': 6, 'dir': 5, 'a': 4, 'b': 17}
right_pins = {'pwm': 26, 'dir': 13, 'a': 22, 'b': 27}

# camera stuff
pink = ((160, 100, 120), (180, 210, 255))
resolution = (320, 240)
min_obj_radius = 5

# pids
servo_pid_constants = {'kp': 0.25, 'ki': 0, 'kd': 0}
motor_pid_constants = {'kp': 0.00102, 'ki': 0.0178333, 'kd': 0}
forward_pid_constants = {'kp': 1, 'ki': 0, 'kd': 0}
angle_pid_constants = {'kp': 1, 'ki': 0, 'kd': 0}

# encoder stuff
encoder_edges_per_rev = 192

# robot dimensions
# all distances in mm and angles in radians
wheel_radius = 42  # 53
wheel_circumference = wheel_radius*2*pi
distance_ratio = wheel_circumference/encoder_edges_per_rev
distance_between_wheels = 400.0
max_wheel_vel = 16*wheel_circumference

current_coefficient = 0.0488

camera_x_offset = 0
camera_y_offset = 0

servo_speed = 1.14
frame_rate = 35
max_move = 2*pi/servo_speed/frame_rate

motor_acceleration_limit = 0.01

target_dist_offset = 700
