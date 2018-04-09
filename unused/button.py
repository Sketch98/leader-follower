import pigpio

from parameters import button_debounce_delay


class ButtonPushedException(Exception):
    pass


class Button:
    """
    Waits for a button to be pressed
    """
    
    def __init__(self, pin):
        global raspi
        raspi.set_mode(pin, pigpio.INPUT)
        self._cb = raspi.callback(pin, pigpio.RISING_EDGE, self._press)
        
        self._last_time = 0.0
    
    def _press(self, gpio, level, tick):
        # convert ns to s
        time = tick/1000000.0
        if time - self._last_time >= button_debounce_delay:
            self._last_time = time
            raise ButtonPushedException
    
    def stop(self):
        self._cb.cancel()


if __name__ == '__main__':
    from time import sleep
    
    
    raspi = pigpio.pi()
    btn = Button(12)
    while True:
        try:
            while True:
                sleep(1)
        except ButtonPushedException:
            print('somebody pushed the button')
        except KeyboardInterrupt:
            break
    btn.stop()
    raspi.stop()
