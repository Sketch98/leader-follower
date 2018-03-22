import pigpio


class RotaryEncoder:
    """Class to decode mechanical rotary encoder pulses."""
    
    def __init__(self, pi, gpio_a, gpio_b, gpio_x):
        
        self.pi = pi
        self.gpio_a = gpio_a
        self.gpio_b = gpio_b
        self.gpio_x = gpio_x
        
        self.last_gpio = None
        self.last_level = None
        self.pos = 0
        self.last_pos = 0
        
        self.pi.set_mode(gpio_a, pigpio.INPUT)
        self.pi.set_mode(gpio_b, pigpio.INPUT)
        self.pi.set_mode(gpio_x, pigpio.INPUT)
        
        self.pi.set_pull_up_down(gpio_a, pigpio.PUD_UP)
        self.pi.set_pull_up_down(gpio_b, pigpio.PUD_UP)
        self.pi.set_pull_up_down(gpio_x, pigpio.PUD_UP)
        
        self.lev_a = self.pi.read(gpio_a)
        self.lev_b = self.pi.read(gpio_b)
        
        self.cb_a = self.pi.callback(gpio_a, pigpio.EITHER_EDGE, self._pulse)
        self.cb_b = self.pi.callback(gpio_b, pigpio.EITHER_EDGE, self._pulse)
        self.cb_x = self.pi.callback(gpio_x, pigpio.RISING_EDGE, self._report)
    
    def _pulse(self, gpio, level, tick):
        if gpio == self.last_gpio and level == self.last_level:  # debounce
            return
        self.last_gpio = gpio
        self.last_level = level
        
        if gpio == self.gpio_a:
            self.lev_a = level
            if level == self.lev_b:
                self.pos += 1
            else:
                self.pos -= 1
        elif gpio == self.gpio_b:
            self.lev_b = level
            if level == self.lev_a:
                self.pos -= 1
            else:
                self.pos += 1
    
    def _report(self, gpio, level, tick):
        print("pos={}, dif={}".format(self.pos, self.pos - self.last_pos))
        self.last_pos = self.pos
    
    def zero(self):
        self.pos = 0
    
    def get_pos(self):
        return self.pos
    
    def cancel(self):
        # Cancel the rotary encoder callback
        self.cb_a.cancel()
        self.cb_b.cancel()
        self.cb_x.cancel()


if __name__ == "__main__":
    import time
    
    pi = pigpio.pi()
    encoder = RotaryEncoder(pi, 23, 18, 24)
    encoder = RotaryEncoder(pi, 17, 27, 22)
    time.sleep(300)
    encoder.cancel()
    pi.stop()
