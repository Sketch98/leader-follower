from time import time


class Timer:
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
