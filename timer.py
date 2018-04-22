from time import time


class Timer:
    """A wrapper for time.time() that tells you how long its been since you last
    checked. Also allows you to set a lower_limit for the time that has passed
    and will return None if the lower_limit amount of time hasn't passed yet."""
    def __init__(self, lower_limit=0.0):
        self.t = time()
        self.lower_limit = lower_limit
    
    def start(self):
        self.t = time()
    
    def elapsed(self):
        dif = time() - self.t
        if dif < self.lower_limit:
            return None
        self.t += dif
        return dif
    
    def reset(self):
        self.t = time()
