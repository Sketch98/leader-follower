from math import pi

# ------------------------------ parameters ------------------------------
# camera stuff
pink = ((160, 100, 120), (180, 210, 255))
resolution = (640, 480)
min_obj_radius = 5

# pids
servo_pid_constants = {'kp': 0.3, 'ki': 0, 'kd': 0.25}
motor_pid_constants = {'kp': 0.00102, 'ki': 0.0178333, 'kd': 0}
forward_pid_constants = {'kp': 1, 'ki': 0, 'kd': 0.2}
angle_pid_constants = {'kp': 1, 'ki': 0, 'kd': 0.2}

target_dist_offset = 700
small_angle = pi/36
nav_timer_interval = 0.01

button_delay = 0.3

# ------------------------------ constants ------------------------------
# pins
servo_pin = 25
left_pins = {'pwm': 6, 'dir': 5, 'a': 17, 'b': 27}
right_pins = {'pwm': 26, 'dir': 13, 'a': 23, 'b': 18}

frame_rates = {(320, 240): 33, (640, 480): 12, (1280, 720): 5, (1920, 1080): 2}
frame_rate = frame_rates[resolution]
servo_speed = 1.67
max_move = 2*pi/servo_speed/frame_rate

# converts 10 bit adc to current in amps
current_coefficient = 0.0488
current_time_limit = 500

# also equal to the pos_dif per rev
encoder_edges_per_rev = 192

# robot dimensions
# all distances in mm and angles in radians
wheel_radius = 50  # 42
wheel_circumference = wheel_radius*2*pi
distance_ratio = wheel_circumference/encoder_edges_per_rev
distance_between_wheels = 400
max_wheel_vel = 16*wheel_circumference

# x and y distance from center of wheels to center of camera servo
camera_x_offset = 0
camera_y_offset = 0
# distance from center of camera servo to camera sensor
camera_dist_offset = 0

motor_pwm_range = 40000
