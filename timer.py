from time import time


class Timer:
    def __init__(self):
        self.t = time()
        self.f = open('b.csv', 'w')
    
    def start(self):
        self.t = time()
    
    def elapsed(self, update=True):
        dif = time() - self.t
        if update:
            self.t += dif
        if dif < 0.8:
            self.f.write('{}\n'.format(dif))
        return dif
    
    def close(self):
        self.f.close()
