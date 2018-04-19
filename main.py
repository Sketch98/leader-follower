from time import sleep
from threading import Condition

from globals import raspi
from nav_system import NavSystem
from pi_video_stream import PiVideoStream
from button import Button
from parameters import button_pin


nav_system = NavSystem()
cond = Condition()


def pvs_callback(dist, camera_to_ball_angle):
    nav_system.update_ball_pos(dist, camera_to_ball_angle)


def button_callback():
    with cond:
        cond.notify()


pvs = PiVideoStream(pvs_callback)
button = Button(button_pin, button_callback)
nav_system.start()
pvs.start()
try:
    while True:
        with cond:
            cond.wait()
        print('WHY DID YOU PRESS THE BUTTON!')
        nav_system.pause()
        sleep(15)
        nav_system.resume()
except KeyboardInterrupt:
    print("somebody ctrl+c'd me :^(")
finally:
    pvs.stop()
    nav_system.stop()
    button.stop()
    raspi.stop()
