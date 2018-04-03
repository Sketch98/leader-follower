import pigpio
from parameters import button_delay

class Button:
    """
    Waits for a button to be pressed
    """
    
    def __init__(self, raspi, pin, callback):
        self.raspi = raspi
        self.raspi.set_mode(pin, pigpio.INPUT)
        self.cb = self.raspi.callback(pin, pigpio.RISING_EDGE, self._press)
        
        self.callback = callback
        self.last_time = 0.0
    
    def _press(self, gpio, level, tick):
        # convert ns to s
        time = tick/1000000.0
        if time - self.last_time >= button_delay:
            self.last_time = time
            self.callback()
    
    def stop(self):
        self.cb.cancel()


if __name__ == '__main__':
    from time import sleep
    
    
    def callback():
        print('someone pressed the button')
    
    
    raspi = pigpio.pi()
    btn = Button(raspi, 12, callback)
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        btn.stop()
        raspi.stop()
