import pigpio

from parameters import motor_pwm_range


class Motor:
    def __init__(self, pwm_pin, dir_pin, forward):
        self._pwm_pin = pwm_pin
        self._dir_pin = dir_pin
        self._forward = forward
        
        global raspi
        raspi.set_mode(pwm_pin, pigpio.OUTPUT)
        raspi.set_mode(dir_pin, pigpio.OUTPUT)
        raspi.set_PWM_range(pwm_pin, motor_pwm_range)
        self._set_pwm(0)
    
    def _set_dir(self, direction):
        global raspi
        assert direction in [0, 1], 'invalid direction = {} in _set_dir'.format(direction)
        raspi.write(self._dir_pin, direction)
    
    def _set_pwm(self, pwm):
        global raspi
        pwm = max(min(pwm, 5000), -5000)
        assert motor_pwm_range >= pwm >= 0, 'invalid pwm = {} in _set_pwm'.format(pwm)
        raspi.set_PWM_dutycycle(self._pwm_pin, int(pwm))
    
    def stop(self):
        self._set_pwm(0)
    
    def set_speed(self, speed):
        if speed >= 0:
            self._set_dir(self._forward)
        else:
            self._set_dir(self._forward ^ 1)
        self._set_pwm(abs(speed)*motor_pwm_range)


if __name__ == "__main__":
    import time
    from rotary_encoder import RotaryEncoder
    from parameters import left_pins, right_pins
    
    raspi = pigpio.pi()
    left_motor = Motor(left_pins['pwm'], left_pins['dir'], 0)
    right_motor = Motor(right_pins['pwm'], right_pins['dir'], 1)
    left_enc = RotaryEncoder(left_pins['a'], left_pins['b'])
    right_enc = RotaryEncoder(right_pins['a'], right_pins['b'])
    
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
        raspi.stop()
