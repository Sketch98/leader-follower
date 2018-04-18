from picamera import PiCamera
from picamera.array import PiRGBArray
from numpy import mean

from globals import limit
from timer import Timer

timer = Timer()
timer.start()

# proportional term to tune
p = 0.01
with PiCamera() as camera:
    camera.resolution = (1280, 720)
    camera.awb_mode = 'off'
    rg, bg = (1.165, 2.44)
    camera.awb_gains = (rg, bg)
    with PiRGBArray(camera, size=(128, 72)) as output:
        # Allow 30 attempts to fix AWB
        for i in range(10):
            # Capture a tiny resized image in RGB format, and extract the
            # average R, G, and B values
            camera.capture(output, format='bgr', resize=(128, 72), use_video_port=True)
            h1, g, r = (mean(output.array[..., i]) for i in range(3))
            print('rg: {} bg: {} rgb: ({}, {},{})'.format(rg, bg, r, g, h1))
            dif = (g - r)*p
            rg += dif
            dif = (g - h1)*p
            bg += dif
            rg = limit(rg, 0, 8)
            bg = limit(bg, 0, 8)
            camera.awb_gains = (rg, bg)
            output.seek(0)
            output.truncate()
print(timer.elapsed())
