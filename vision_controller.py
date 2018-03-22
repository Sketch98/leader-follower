from vision import Vision
from time import time


class VisionController:
    def __init__(self, resolution):
        self.resolution = resolution
        self.vision = Vision(resolution, 10)
        self.callback = None
    
    def set_callback(self, callback):
        self.callback = callback
    
    def loop(self):
        assert self.callback is not None, 'must have callback function before starting vision loop'
        last_time = time()
        while True:
            self.vision.grab_frame()
            x = self.vision.get_x()
            # y = self.vision.get_y()
            diameter = self.vision.get_diameter()
            self.callback(x, diameter, self.resolution[0])
            
            cur_time = time()
            if cur_time!= last_time:
                print('fps {}   x {}   diameter {}'.format(1.0/(cur_time - last_time), x, diameter))
            last_time = cur_time
