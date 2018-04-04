import time

import cv2
from imutils.video import VideoStream

from parameters import min_obj_radius, pink, resolution


class Vision:
    def __init__(self):
        # initialize the video stream and allow the camera sensor to warm up
        self._vs = VideoStream(usePiCamera=True, resolution=resolution).start()
        time.sleep(2.0)
    
    def _analyze_frame(self):
        # grab the current frame and convert it to the HSV color space
        frame = self._vs.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # construct a mask for the color pink, then perform a series of
        # dilations and erosions to remove any small blobs left in the mask
        mask = cv2.inRange(hsv, pink[0], pink[1])
        # mask = cv2.erode(mask, None, iterations=1)
        # mask = cv2.dilate(mask, None, iterations=1)
        
        # find contours in the mask
        contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        
        x = -1
        y = -1
        diameter = -1
        # only proceed if at least one contour was found
        if len(contours) > 0:
            # find the largest contour in the mask, then use it to compute
            # the minimum enclosing circle and centroid
            c = max(contours, key=cv2.contourArea)
            ((x_pix, y_pix), radius) = cv2.minEnclosingCircle(c)
            
            # only proceed if the radius meets a minimum size
            if radius >= min_obj_radius:
                x = resolution[0] - x_pix
                y = y_pix
                diameter = radius*2
        
        return x, y, diameter
    
    def loop(self, callback):
        while True:
            # not using the y position of the ball in frame currently
            x, _, diameter = self._analyze_frame()
            callback(x, diameter)
    
    def stop(self):
        self._vs.stop()
