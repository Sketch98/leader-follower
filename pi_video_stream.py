from threading import Thread
from picamera import PiCamera
from picamera.array import PiRGBArray


class PiVideoStream:
    def __init__(self, awb_gains, resolution, frame_rate=32):
        # initialize the camera and stream
        self._camera = PiCamera()
        self._camera.resolution = resolution
        self._camera.framerate = frame_rate
        self._camera.awb_mode = 'off'
        self._camera.awb_gains = awb_gains
        self._rawCapture = PiRGBArray(self._camera, size=resolution)
        self._stream = self._camera.capture_continuous(self._rawCapture,
                                                       format='bgr', use_video_port=True)
        
        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.frame = None
        self._stopped = False
    
    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update)
        t.daemon = True
        t.start()
        return self
    
    def update(self):
        # keep looping infinitely until the thread is stopped
        for f in self._stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = f.array
            self._rawCapture.truncate(0)
            
            # if the thread indicator variable is set, stop the thread
            # and resource camera resources
            if self._stopped:
                self._stream.close()
                self._rawCapture.close()
                self._camera.close()
                return
    
    def read(self):
        # return the frame most recently read
        return self.frame
    
    def stop(self):
        # indicate that the thread should be stopped
        self._stopped = True
