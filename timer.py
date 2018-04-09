from time import time

from log_decorator import LogDecorator

class Timer:
    def __init__(self):
        self.t = time()
    
    def start(self):
        self.t = time()
    
    @LogDecorator('b.csv')
    def elapsed(self, update=True):
        dif = time() - self.t
        if update:
            self.t += dif
        return dif
    
    def close(self):
        self.elapsed.close()
