import pigpio

from globals import raspi


class RotaryEncoder:
    """
    decodes quadrature signal from a rotary encoder
    """
    
    def __init__(self, a, b):
        self._a = a
        self._b = b
        
        self._last_gpio = None
        self._last_level = None
        self._last_pos = 0
        self.pos = 0
        
        raspi.set_mode(a, pigpio.INPUT)
        raspi.set_mode(b, pigpio.INPUT)
        
        raspi.set_pull_up_down(a, pigpio.PUD_UP)
        raspi.set_pull_up_down(b, pigpio.PUD_UP)
        
        self._lev_a = raspi.read(a)
        self._lev_b = raspi.read(b)
        
        self._cb_a = raspi.callback(a, pigpio.EITHER_EDGE, self._pulse)
        self._cb_b = raspi.callback(b, pigpio.EITHER_EDGE, self._pulse)
    
    def _pulse(self, gpio, level, tick):
        # debounce
        if gpio == self._last_gpio and level == self._last_level:
            return
        self._last_gpio = gpio
        self._last_level = level
        
        if gpio == self._a:
            self._lev_a = level
            if level == self._lev_b:
                self.pos += 1
            else:
                self.pos -= 1
        elif gpio == self._b:
            self._lev_b = level
            if level == self._lev_a:
                self.pos -= 1
            else:
                self.pos += 1
    
    def get_pos_dif(self):
        pos_dif = self.pos - self._last_pos
        self._last_pos += pos_dif
        return pos_dif
    
    def reset(self):
        self._last_pos = self.pos
    
    def stop(self):
        # Cancel the rotary encoder callback
        self._cb_a.cancel()
        self._cb_b.cancel()


if __name__ == "__main__":
    import time
    from parameters import left_pins
    
    encoder = RotaryEncoder(left_pins['a'], left_pins['b'])
    try:
        while True:
            print(encoder.get_pos_dif())
            print(encoder.pos)
            time.sleep(0.01)
    except KeyboardInterrupt:
        encoder.stop()
        raspi.stop()
