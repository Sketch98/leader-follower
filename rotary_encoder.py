import pigpio


class RotaryEncoder:
    """
    decodes quadrature signal from a rotary encoder
    """
    
    def __init__(self, pi, a, b):
        
        self.pi = pi
        self.gpio_a = a
        self.gpio_b = b
        # self.gpio_x = x
        
        self.last_gpio = None
        self.last_level = None
        self.pos = 0
        self.last_pos = 0
        
        self.pi.set_mode(a, pigpio.INPUT)
        self.pi.set_mode(b, pigpio.INPUT)
        # self.pi.set_mode(x, pigpio.INPUT)
        
        self.pi.set_pull_up_down(a, pigpio.PUD_UP)
        self.pi.set_pull_up_down(b, pigpio.PUD_UP)
        # self.pi.set_pull_up_down(x, pigpio.PUD_UP)
        
        self.lev_a = self.pi.read(a)
        self.lev_b = self.pi.read(b)
        
        self.cb_a = self.pi.check_current(a, pigpio.EITHER_EDGE, self._pulse)
        self.cb_b = self.pi.check_current(b, pigpio.EITHER_EDGE, self._pulse)
        # self.cb_x = self.pi.check_current(x, pigpio.RISING_EDGE, self._report)
    
    def _pulse(self, gpio, level, tick):
        # debounce
        if gpio == self.last_gpio and level == self.last_level:
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
    
    # def _report(self, gpio, level, tick):
    #     print("pos={}, dif={}".format(self.pos, self.pos - self.last_pos))
    #     self.last_pos = self.pos
    
    def zero(self):
        self.pos = 0
    
    def get_pos(self):
        return self.pos
    
    def get_pos_dif(self):
        pos = self.get_pos()
        pos_dif = pos - self.last_pos
        self.last_pos = pos
        return pos_dif
    
    def stop(self):
        # Cancel the rotary encoder callback
        self.cb_a.cancel()
        self.cb_b.cancel()
        # self.cb_x.cancel()

