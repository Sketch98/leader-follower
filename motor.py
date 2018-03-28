import pigpio


class Motor:
    def __init__(self, pi, pwm_pin, dir_pin, pwm_range=40000, forward=1):
        self.pi = pi
        self.pwm_pin = pwm_pin
        self.dir_pin = dir_pin
        self.pwm_range = pwm_range
        self.forward = forward
        
        self.pi.set_mode(pwm_pin, pigpio.OUTPUT)
        self.pi.set_PWM_range(pwm_pin, pwm_range)
        self.pi.set_mode(dir_pin, pigpio.OUTPUT)
        self.stop()
    
    def _set_dir(self, direction):
        assert direction in [0, 1], 'invalid direction = {} in _set_dir'.format(direction)
        self.pi.write(self.dir_pin, direction)
    
    def _set_pwm(self, pwm):
        assert self.pwm_range >= pwm >= 0, 'invalid pwm = {} in _set_pwm'.format(pwm)
        self.pi.set_PWM_dutycycle(self.pwm_pin, int(pwm))
    
    def stop(self):
        self.pi.set_PWM_dutycycle(self.pwm_pin, 0)
    
    def set_speed(self, speed):
        if speed >= 0:
            self._set_dir(self.forward)
        else:
            self._set_dir(self.forward ^ 1)
        self._set_pwm(abs(speed)*self.pwm_range)


if __name__ == "__main__":
    import time
    from rotary_encoder import RotaryEncoder
    
    pi = pigpio.pi()
    
    left_pins = {'pwm': 6, 'dir': 5, 'a': 4, 'b': 17}
    right_pins = {'pwm': 26, 'dir': 13, 'a': 22, 'b': 27}
    left_motor = Motor(pi, 6, 5, forward=0)
    right_motor = Motor(pi, 26, 13)
    left_enc = RotaryEncoder(pi, 4, 17)
    right_enc = RotaryEncoder(pi, 22, 27)
    
    base_speed = 20
    for speed in range(0, base_speed + 1, 1):
        left_motor.set_speed(speed/100.0)
        right_motor.set_speed(speed/100.0)
        time.sleep(0.1)
    limit_speed = 40
    time.sleep(1)
    try:
        while True:
            for speed in range(base_speed, limit_speed + 1, 1):
                left_motor.set_speed(speed/100.0)
                right_motor.set_speed(speed/100.0)
                time.sleep(0.1)
                print(left_enc.get_pos_dif())
                print(right_enc.get_pos_dif())
                print(speed)
                print('')
            for speed in range(0, limit_speed - base_speed + 1, 1):
                left_motor.set_speed((limit_speed - speed)/100.0)
                right_motor.set_speed((limit_speed - speed)/100.0)
                time.sleep(0.1)
                print(left_enc.get_pos_dif())
                print(right_enc.get_pos_dif())
                print(speed)
                print('')
    except KeyboardInterrupt:
        pass
    finally:
        left_motor.stop()
        right_motor.stop()
        left_enc.stop()
        right_enc.stop()
        pi.stop()
