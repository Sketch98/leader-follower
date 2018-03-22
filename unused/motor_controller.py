import pigpio
from motor import Motor
from rotary_encoder import RotaryEncoder


class MotorController:
    def __init__(self, pi, motor_pins, encoder_pins, pid_constants, pwm_range=255, forward=1):
        motor = Motor(pi, motor_pins['pwm'], motor_pins['dir'], pwm_range=pwm_range, forward=forward)
        encoder = RotaryEncoder(pi, encoder_pins['a'], encoder_pins['b'], encoder_pins['x'])


if __name__ == '__main__':
    pi = pigpio.pi()
    motor_pins = {'pwm': 6, 'dir': 5}
    encoder_pins = {'a': 23, 'b': 18, 'x': 24}
    pid_pins = {'kp': 1.0, 'ki': 1.0, 'kd': 1.0, 'min_i': 1.0, 'max_i': 1.0}
    motor_controller = MotorController(pi, motor_pins, encoder_pins)
