import pigpio


class Motor:
    def __init__(self, pi, pwm_pin, dir_pin, pwm_range=255, forward=1):
        self.pi = pi
        self.pwm_pin = pwm_pin
        self.dir_pin = dir_pin
        self.pwm_range = pwm_range
        self.forward = forward

        self.pi.set_mode(pwm_pin, pigpio.OUTPUT)
        self.pi.set_PWM_range(pwm_pin, pwm_range)
        self.pi.set_mode(dir_pin, pigpio.OUTPUT)
        self.off()
    
    def set_dir(self, direction):
        assert direction in [0, 1], 'invalid direction = {} in set_dir'.format(direction)
        self.pi.write(self.dir_pin, direction)
    
    def set_pwm(self, pwm):
        assert self.pwm_range >= pwm >= 0, 'invalid pwm = {} in set_pwm'.format(pwm)
        self.pi.set_PWM_dutycycle(self.pwm_pin, int(pwm))
    
    def set_pwm_percent(self, pwm):
        self.pi.set_PWM_dutycycle(self.pwm_pin, pwm)
    
    def off(self):
        self.pi.set_PWM_dutycycle(self.pwm_pin, 0)
    
    def set_speed(self, speed):
        assert 1.0 >= speed >= -1.0, 'invalid speed = {} in set_speed'.format(speed)
        if speed >= 0:
            self.set_dir(self.forward)
        else:
            self.set_dir(self.forward ^ 1)
        self.set_pwm(abs(speed)*self.pwm_range)


if __name__ == "__main__":
    import time
    from rotary_encoder import RotaryEncoder
    from servo_controller import ServoController
    
    pi = pigpio.pi()
    servo_controller = ServoController(pi, 25, 180, 0, 90)
    servo_controller.off()

    def callback(pos, dif):
        pass
        # print("pos={}, dif={}".format(pos, dif))
    
    right_motor = Motor(pi, 6, 5)
    left_motor = Motor(pi, 26, 13)
    right_enc = RotaryEncoder(pi, 23, 18, 24, callback)
    left_enc = RotaryEncoder(pi, 17, 27, 22, callback)
    
    base_speed = 20
    for speed in range(0, base_speed + 1, 1):
        right_motor.set_speed(speed / 100.0)
        left_motor.set_speed(-speed / 100.0)
        time.sleep(0.1)
    limit_speed = 40
    time.sleep(1)
    try:
        while True:
            for speed in range(base_speed, limit_speed + 1, 1):
                right_motor.set_speed(speed/100.0)
                left_motor.set_speed(-speed/100.0)
                time.sleep(0.1)
            for speed in range(0, base_speed + 1, 1):
                right_motor.set_speed((limit_speed - speed) / 100.0)
                left_motor.set_speed(-(limit_speed - speed) / 100.0)
                time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        left_motor.off()
        right_motor.off()
        left_enc.cancel()
        right_enc.cancel()
        pi.stop()
