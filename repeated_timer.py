import time
from threading import Event, Thread


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
            self._func()
    
    def _time(self):
        time_elapsed = time.time() - self._last_time
        self._last_time += time_elapsed
        assert self._interval > time_elapsed, 'drive_system loop took {}s which is longer than longer than' \
                                              'the allowed interval {}s'.format(time_elapsed, self._interval)
        return self._interval - time_elapsed
    
    def start(self):
        self._last_time = time.time()
        self._thread.start()
    
    def stop(self):
        self._event.set()
        self._thread.join()
