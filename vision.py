from math import asin, tan, sqrt
from time import sleep

import cv2
from imutils.video import VideoStream

from parameters import min_obj_radius, pink, resolution


class Vision:
    def __init__(self):
        # initialize the video stream and allow the camera sensor to warm up
        self._vs = VideoStream(usePiCamera=True, resolution=resolution)
    
    def _analyze_frame(self):
        # grab the current frame and convert it to the HSV color space
        hsv = cv2.cvtColor(self._vs.read(), cv2.COLOR_BGR2HSV)
        
        # construct a mask for the color pink
        mask = cv2.inRange(hsv, pink[0], pink[1])
        
        # find contours in the mask
        contours = \
            cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[
                -2]
        
        x, y, radius = None, None, None
        # only proceed if at least one contour was found
        if len(contours) > 0:
            # find the largest contour in the mask, then use it to compute
            # the minimum enclosing circle and centroid
            c = max(contours, key=cv2.contourArea)
            ((x_pix, y_pix), r_pix) = cv2.minEnclosingCircle(c)
            
            # only proceed if the radius meets a minimum size
            if radius >= min_obj_radius:
                x = x_pix
                y = y_pix
                radius = r_pix
        
        return x, y, radius
    
    def dist_angle_to_ball(self):
        """
        finds the angles to the left and right sides of the ball.
        it uses that to estimate the distance and angle to the ball.
        """
        x, y, radius = self._analyze_frame()
        # return None if ball not in frame
        if x is None:
            return None, None
        
        x -= resolution[0]/2
        y -= resolution[1]/2
        r = sqrt(x*x + y*y)
        
        # corrects for camera's lens projecting curved light onto a flat sensor
        left_angle = 2*asin(0.4672*(r - radius)/resolution[0])
        right_angle = 2*asin(0.4672*(r + radius)/resolution[0])
        
        ball_x_angle = (right_angle + left_angle)/2*x/r
        dist = 33.1/abs(tan((right_angle - left_angle)/2))
        return dist, ball_x_angle
    
    def dist_angle_to_ball_simple(self):
        """
        estimates the distance and angle to the ball
        """
        # not using the y position of the ball in frame currently
        x, _, radius = self._analyze_frame()
        # return None if ball not in frame
        if x is None:
            return None, None
        
        ball_x_angle = (x - 0.5)*0.9326/resolution[0]
        dist = 33.1/tan(radius*0.9326/resolution[0])
        return dist, ball_x_angle
    
    def start(self):
        self._vs.start()
        sleep(2)
    
    def stop(self):
        self._vs.stop()
