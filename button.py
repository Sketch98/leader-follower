import pigpio


class Button:
    """
    Waits for a button to be pressed
    """
    
    def __init__(self, pi, pin, callback, delay=0.5):
        self.pi = pi
        self.pi.set_mode(pin, pigpio.INPUT)
        self.cb = self.pi.callback(pin, pigpio.RISING_EDGE, self._press)
        
        self.callback = callback
        self.delay = delay
        self.last_time = 0.0
    
    def _press(self, gpio, level, tick):
        # convert ns to s
        time = tick/1000000.0
        if time - self.last_time >= self.delay:
            self.last_time = time
            self.callback()
    
    def stop(self):
        # Cancel the rotary encoder callback
        self.cb.cancel()


if __name__ == '__main__':
    from time import sleep
    
    
    def callback():
        print('someone pressed the button')
    
    
    pi = pigpio.pi()
    btn = Button(pi, 12, callback)
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        btn.stop()
        pi.stop()
