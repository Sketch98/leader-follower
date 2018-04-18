from math import asin, tan
from time import sleep
from threading import Thread

import cv2
from parameters import camera_dist_offset, min_obj_radius, resolution, awb_gains, pink, resolution, awb_gains
from picamera import PiCamera
from picamera.array import PiRGBArray


def angle_to_pixel(x_pix):
    # corrects for camera's lens projecting curved light onto a flat sensor
    angle = asin(0.8643*(x_pix/resolution[0] - 0.5))
    return angle


def dist_angle_to_ball(x, diameter):
    """
    finds the angles to the left and right sides of the ball.
    it uses that to estimate the distance and angle to the ball.
    """
    # return None if ball not in frame
    if x is None:
        return None, None
    
    left_angle = angle_to_pixel(x - diameter/2.0)
    right_angle = angle_to_pixel(x + diameter/2.0)
    ball_angle = (right_angle + left_angle)/2
    dist = abs(33.1/tan(right_angle - left_angle)) + camera_dist_offset
    return dist, ball_angle


class PiVideoStream:
    def __init__(self, callback, display=False):
        # initialize the camera and stream
        self._camera = PiCamera()
        self._camera.resolution = resolution
        self._camera.framerate = 42.1
        self._camera.awb_mode = 'off'
        self._camera.awb_gains = awb_gains
        self._camera.iso = 200
        self._rawCapture = PiRGBArray(self._camera, size=resolution)
        self._stream = self._camera.capture_continuous(self._rawCapture,
                                                       format='bgr', use_video_port=True)
        
        self._stopped = False
        self.pink = pink
        self.callback = callback
        self._display = display
    
    def set_iso(self, iso):
        self._camera.iso = iso
    
    def set_awb_gains(self, awb_gains):
        self._camera.awb_gains = awb_gains
    
    def analyze_frame(self, frame):
        # convert the frame to the HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # construct a mask for the color pink
        mask = cv2.inRange(hsv, self.pink[0], self.pink[1])
        # mask = cv2.erode(mask, None, iterations=1)
        # mask = cv2.dilate(mask, None, iterations=1)
        
        # find contours in the mask
        contours = \
            cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[
                -2]
        
        x, diameter = None, None
        # only proceed if at least one contour was found
        if len(contours) > 0:
            # find the largest contour in the mask, then use it to compute
            # the minimum enclosing circle and centroid
            c = max(contours, key=cv2.contourArea)
            ((x_pix, y_pix), radius) = cv2.minEnclosingCircle(c)
            
            # only proceed if the radius meets a minimum size
            if radius >= min_obj_radius:
                x = x_pix
                diameter = radius*2
        
        if self._display:
            cv2.imshow('frame', frame)
            cv2.imshow('hsv', hsv)
            cv2.imshow('mask', mask)
            cv2.waitKey(1) & 0xFF
        
        return x, diameter
    
    def _target(self):
        # keep looping infinitely until the thread is stopped
        for f in self._stream:
            # if the thread indicator variable is set, stop the thread
            # and camera resources
            if self._stopped:
                self._stream.close()
                self._rawCapture.close()
                self._camera.close()
                return
            
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            frame = f.array
            self._rawCapture.truncate(0)
            # process the image and send it out
            x, diameter = self.analyze_frame(frame)
            dist, angle = dist_angle_to_ball(x, diameter)
            self.callback(dist, angle)
    
    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self._target)
        t.daemon = True
        t.start()
        sleep(2)
    
    def stop(self):
        # indicate that the thread should be stopped
        self._stopped = True
