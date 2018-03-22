import pigpio


class Motor:
    def __init__(self, pi, pwm_pin, dir_pin, pwm_range=255, forward=1, limit=0.5):
        self.pi = pi
        self.pwm_pin = pwm_pin
        self.dir_pin = dir_pin
        self.pwm_range = pwm_range
        self.forward = forward
        self.limit = limit
        
        self.pi.set_mode(pwm_pin, pigpio.OUTPUT)
        self.pi.set_PWM_range(pwm_pin, pwm_range)
        self.pi.set_mode(dir_pin, pigpio.OUTPUT)
        self.stop()
    
    def _set_dir(self, direction):
        assert direction in [0, 1], 'invalid direction = {} in _set_dir'.format(direction)
        self.pi.write(self.dir_pin, direction)
    
    def _set_pwm(self, pwm):
        assert self.pwm_range >= pwm >= 0, 'invalid pwm = {} in _set_pwm'.format(pwm)
        self.pi.set_PWM_dutycycle(self.pwm_pin, int(min(pwm, self.pwm_range*self.limit)))
    
    def stop(self):
        self.pi.set_PWM_dutycycle(self.pwm_pin, 0)
    
    def set_speed(self, speed):
        if speed >= 0:
            self._set_dir(self.forward)
        else:
            self._set_dir(self.forward ^ 1)
        self._set_pwm(abs(speed)*self.pwm_range)

