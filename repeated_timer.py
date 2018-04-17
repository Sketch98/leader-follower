from threading import Event, Thread
from time import time


class RepeatedTimer:
    """Repeat `func` every `interval` seconds."""
    
    def __init__(self, interval, func):
        self._interval = interval
        self._func = func
        self._last_time = 0
        self._event = Event()
        self._thread = Thread(target=self._target)
    
    def _target(self):
        while not self._event.wait(self._time()):
            time_elapsed = time() - self._last_time
            self._last_time += time_elapsed
            self._func(time_elapsed)
    
    def _time(self):
        time_elapsed = time() - self._last_time
        if self._interval < time_elapsed:
            # print('repeated_timer took {}, which is longer than interval {}'.format(time_elapsed, self._interval))
            return 0
        return self._interval - time_elapsed
    
    def start(self):
        self._last_time = time()
        self._thread.start()
    
    def stop(self):
        self._event.set()
        self._thread.join()


if __name__ == '__main__':
    from time import sleep
    
    
    def say_hello(interval):
        print('hello, it has been {}s'.format(interval))
    
    
    repeated_timer = RepeatedTimer(0.1, say_hello)
    repeated_timer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        repeated_timer.stop()
