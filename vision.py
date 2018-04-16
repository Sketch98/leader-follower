from math import asin, tan
from time import sleep

import cv2
from imutils.video import VideoStream

from parameters import camera_dist_offset, min_obj_radius, pink, resolution


def angle_to_pixel(x_pix):
    # corrects for camera's lens projecting curved light onto a flat sensor
    angle = asin(0.8643*(x_pix/resolution[0] - 0.5))
    return angle


class Vision:
    def __init__(self):
        # initialize the video stream and allow the camera sensor to warm up
        self._vs = VideoStream(usePiCamera=True, resolution=resolution)
    
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
        contours = \
            cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[
                -2]
        
        x, y, diameter = None, None, None
        # only proceed if at least one contour was found
        if len(contours) > 0:
            # find the largest contour in the mask, then use it to compute
            # the minimum enclosing circle and centroid
            c = max(contours, key=cv2.contourArea)
            ((x_pix, y_pix), radius) = cv2.minEnclosingCircle(c)
            
            # only proceed if the radius meets a minimum size
            if radius >= min_obj_radius:
                x = x_pix
                y = y_pix
                diameter = radius*2
        
        # cv2.imshow('frame', frame)
        # cv2.imshow('mask', mask)
        # cv2.waitKey(1) & 0xFF
        
        return x, y, diameter
    
    def dist_angle_to_ball(self):
        """
        finds the angles to the left and right sides of the ball.
        it uses that to estimate the distance and angle to the ball.
        """
        # not using the y position of the ball in frame currently
        x_pix, _, diameter = self._analyze_frame()
        # return None if ball not in frame
        if x_pix is None:
            return None, None
        
        left_angle = angle_to_pixel(x_pix - diameter/2.0)
        right_angle = angle_to_pixel(x_pix + diameter/2.0)
        ball_angle = (right_angle + left_angle)/2
        dist = abs(33.1/tan(right_angle - left_angle)) + camera_dist_offset
        return dist, ball_angle
    
    def start(self):
        self._vs.start()
        sleep(2)
    
    def stop(self):
        self._vs.stop()
