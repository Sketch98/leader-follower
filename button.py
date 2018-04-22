import pigpio

from parameters import button_debounce_delay
from globals import raspi


class Button:
    """
    Waits for a button to be pressed
    """
    
    def __init__(self, pin, callback, active_low=True):
        raspi.set_mode(pin, pigpio.INPUT)
        if active_low:
            raspi.set_pull_up_down(pin, pigpio.PUD_UP)
            self._cb = raspi.callback(pin, pigpio.FALLING_EDGE, self._press)
        else:
            raspi.set_pull_up_down(pin, pigpio.PUD_DOWN)
            self._cb = raspi.callback(pin, pigpio.RISING_EDGE, self._press)
        
        self._last_time = 0.0
        self.callback = callback
    
    def _press(self, gpio, level, tick):
        # convert ns to s
        time = tick/1000000.0
        # debounce the button
        if time - self._last_time >= button_debounce_delay:
            self._last_time = time
            self.callback()
    
    def stop(self):
        self._cb.cancel()


if __name__ == '__main__':
    from time import sleep
    
    def callback():
        print('somebody pressed the button')
    
    btn = Button(22, callback)
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        pass
    finally:
        btn.stop()
        raspi.stop()
