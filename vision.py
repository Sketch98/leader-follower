import cv2
from imutils.video import VideoStream
import time


class Vision:
    def __init__(self, pink, resolution, min_obj_width):
        self.pink = pink
        self.min_obj_width = min_obj_width
        
        # initialize the video stream and allow the camera sensor to warm up
        self.vs = VideoStream(usePiCamera=True, resolution=resolution).start()
        time.sleep(2.0)
    
    def analyze_frame(self):
        # grab the current frame
        frame = self.vs.read()
        
        # blur the frame and convert it to the HSV color space
        # frame = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # construct a mask for the color pink, then perform a series of
        # dilations and erosions to remove any small blobs left in the mask
        mask = cv2.inRange(hsv, self.pink[0], self.pink[1])
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        
        # # dilate then erode to connect close together blobs
        # mask = cv2.dilate(mask, None, iterations=4)
        # mask = cv2.erode(mask, None, iterations=4)
        
        # find contours in the mask
        contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        
        x = -1
        y = -1
        diameter = -1
        # only proceed if at least one contour was found
        if len(contours) > 0:
            # find the largest contour in the mask, then use it to compute the minimum enclosing circle and centroid
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            
            # only proceed if the radius meets a minimum size
            if radius >= self.min_obj_width/2:
                x = x
                y = y
                diameter = (radius * 2)
        
        # commands for displaying to monitor
        # cv2.imshow("Mask", mask)
        # cv2.waitKey(1)
        
        return x, y, diameter
    
    def stop(self):
        self.vs.stop()
