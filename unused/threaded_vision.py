from numpy import sqrt
import argparse
import cv2
from imutils.video import VideoStream
from imutils import resize
import time
from threading import Thread, Event


class Vision:
    def __init__(self, screenwidth, min_obj_width):
        # define the lower and upper boundaries of the "green"
        # ball in the HSV color space, then initialize the
        # list of tracked points
        self.screenwidth = screenwidth
        self.min_obj_radius = min_obj_width
        self.pink_upper = (203, 192, 255)
        self.pink_lower = (147, 112, 147)
        self.diameter = -1
        self.x = -1
        self.y = -1
        
        # construct the argument parse and parse the arguments
        self.ap = argparse.ArgumentParser()
        self.ap.add_argument("-p", "--picamera", type=int, default=1,
                             help="whether or not the Raspberry Pi camera should be used")
        self.ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
        args = vars(self.ap.parse_args())
        self.buffer = args["buffer"]
        
        # initialize the video stream and allow the camera sensor to warm up
        self.vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(640, 480), framerate=32).start()
        time.sleep(2)
        
        self.stopped = False
        self.frame = self.vs.read()
        self.frame_ready = Event()
        self.frame_ready.set()
    
    def start(self):
        th = Thread(target=self.update, args=())
        th.start()
    
    def update(self):
        while True:
            if self.stopped:
                return
            self.frame = self.vs.read()
            self.frame_ready.set()
            print(time.time())
    
    def stop(self):
        self.stopped = True
    
    def read(self):
        return self.frame
    
    def grab_frame(self):
        # grab the current frame
        self.frame_ready.wait()
        self.frame_ready.clear()
        print(time.time())
        frame = self.read()
        #frame = resize(frame, width=self.screenwidth)
        
        # resize the frame, blur it, and convert it to the HSV color space
        # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # construct a mask for the color "pink", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, self.pink_lower, self.pink_upper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        
        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)[-2]
        
        # only proceed if at least one contour was found
        if len(contours) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            m = cv2.moments(c)
            center = (int(m["m10"] / m["m00"]), int(m["m01"] / m["m00"]))
            
            # only proceed if the radius meets a minimum size
            if radius >= self.min_obj_radius:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                           (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
            self.diameter = (radius * 2)
            self.x = x
            self.y = y
        else:
            self.diameter = -1
            self.x = -1
            self.y = -1
    
    def get_diameter(self):
        return self.diameter
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

