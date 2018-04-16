from picamera import PiCamera
from picamera.array import PiRGBArray
from numpy import mean

from globals import limit

# proportional term to tune
p = 0.01
with PiCamera() as camera:
    camera.resolution = (1280, 720)
    camera.awb_mode = 'off'
    rg, bg = (2.0, 2.0)
    camera.awb_gains = (rg, bg)
    with PiRGBArray(camera, size=(128, 72)) as output:
        # Allow 30 attempts to fix AWB
        for i in range(30):
            # Capture a tiny resized image in RGB format, and extract the
            # average R, G, and B values
            camera.capture(output, format='rgb', resize=(128, 72), use_video_port=True)
            r, g, b = (mean(output.array[..., i]) for i in range(3))
            print('R:%5.2f, B:%5.2f = (%5.2f, %5.2f, %5.2f)' % (rg, bg, r, g, b))
            dif = (g - r)*p
            rg += dif
            dif = (g - b)*p
            bg += dif
            rg = limit(rg, 0, 8)
            bg = limit(bg, 0, 8)
            camera.awb_gains = (rg, bg)
            output.seek(0)
            output.truncate()
