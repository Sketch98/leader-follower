import pigpio

from parameters import button_debounce_delay


class ButtonPushedException(Exception):
    pass


class Button:
    """
    Waits for a button to be pressed
    """
    
    def __init__(self, in_pin, out_pin):
        global raspi
        raspi.set_mode(in_pin, pigpio.INPUT)
        raspi.set_mode(out_pin, pigpio.OUTPUT)
        
        raspi.set_pull_up_down(in_pin, pigpio.PUD_DOWN)
        raspi.set_pull_up_down(out_pin, pigpio.PUD_UP)
        
        raspi.write(out_pin, 1)
        
        self._cb = raspi.callback(in_pin, pigpio.RISING_EDGE, self._press)
        
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
