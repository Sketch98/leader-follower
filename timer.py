from time import time


class Timer():
    def __init__(self):
        self.t = time()
    
    def start(self):
        self.t = time()
    
    def elapsed(self, update=True):
        dif = time() - self.t
        if update:
            self.t += dif
        return dif
