import time
from threading import Event, Thread


class RepeatedTimer:
    """Repeat `func` every `interval` seconds."""
    
    def __init__(self, interval, func, *args, **kwargs):
        self.interval = interval
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.start_time = time.time()
        self.event = Event()
        self.thread = Thread(target=self._target)
    
    def _target(self):
        while not self.event.wait(self._time):
            self.func(*self.args, **self.kwargs)
    
    @property
    def _time(self):
        return self.interval
        # return self.interval - ((time.time() - self.start_time) % self.interval)
    
    def start(self):
        self.thread.start()
    
    def stop(self):
        self.event.set()
        self.thread.join()
