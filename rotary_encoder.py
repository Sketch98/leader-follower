import pigpio


class RotaryEncoder:
    """
    decodes quadrature signal from a rotary encoder
    """
    
    def __init__(self, raspi, a, b):
        
        self.raspi = raspi
        self.gpio_a = a
        self.gpio_b = b
        
        self.last_gpio = None
        self.last_level = None
        self.pos = 0
        self.last_pos = 0
        
        self.raspi.set_mode(a, pigpio.INPUT)
        self.raspi.set_mode(b, pigpio.INPUT)
        
        self.raspi.set_pull_up_down(a, pigpio.PUD_UP)
        self.raspi.set_pull_up_down(b, pigpio.PUD_UP)
        
        self.lev_a = self.raspi.read(a)
        self.lev_b = self.raspi.read(b)
        
        self.cb_a = self.raspi.callback(a, pigpio.EITHER_EDGE, self._pulse)
        self.cb_b = self.raspi.callback(b, pigpio.EITHER_EDGE, self._pulse)
    
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


if __name__ == "__main__":
    import time
    
    raspi = pigpio.pi()
    encoder = RotaryEncoder(raspi, 17, 27)
    try:
        while True:
            print(encoder.get_pos_dif())
            print(encoder.get_pos())
            time.sleep(0.01)
    except KeyboardInterrupt:
        encoder.stop()
        raspi.stop()
