import time
from threading import Event, Thread


class RepeatedTimer:
    """Repeat `func` every `interval` seconds."""
    
    def __init__(self, interval, func):
        self.interval = interval
        self.func = func
        self.last_time = 0
        self.event = Event()
        self.thread = Thread(target=self._target)
    
    def _target(self):
        # use self._time instead of self.interval for exact timing
        while not self.event.wait(self.interval):
            self.func(interval=self.interval)
    
    def _time(self):
        time_elapsed = time.time() - self.last_time
        assert self.interval > time_elapsed, 'drive_system loop took {}s which is longer than longer than' \
                                             'the allowed interval {}s'.format(time_elapsed, self.interval)
        return self.interval - time_elapsed
    
    def start(self):
        self.last_time = time.time()
        self.thread.start()
    
    def stop(self):
        self.event.set()
        self.thread.join()
