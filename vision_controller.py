from time import time

from vision import Vision


class VisionController:
    # instantiates the vision system and handles outputting the relevant data
    def __init__(self, pink, resolution):
        self.resolution = resolution
        self.vision = Vision(pink, resolution, 10)
        self.callback = None
    
    def set_callback(self, callback):
        self.callback = callback
    
    def loop(self):
        assert self.callback is not None, 'must have callback function before ' \
                                          'starting vision loop'
        last_time = time()
        while True:
            # not using the y position of the ball in frame currently
            x, _, diameter = self.vision.analyze_frame()
            
            cur_time = time()
            if cur_time != last_time and x > 0:
                print('fps {}   x {}   diameter {}'.format(
                    1.0 / (cur_time - last_time), x, diameter))
            last_time = cur_time
            
            self.callback(x, diameter, self.resolution[0])
