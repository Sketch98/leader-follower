from globals import raspi
from nav_system import NavSystem
from vision import Vision
import parameters
from threading import Thread

from matplotlib.widgets import Slider
import matplotlib.pyplot as plt

a_min = 0
a_max = 255
a_init = 0

slider_a = plt.axes([0.1, 0.05, 0.8, 0.05])
slider_b = plt.axes([0.1, 0.15, 0.8, 0.05])
slider_c = plt.axes([0.1, 0.25, 0.8, 0.05])
slider_d = plt.axes([0.1, 0.35, 0.8, 0.05])
slider_e = plt.axes([0.1, 0.45, 0.8, 0.05])
slider_f = plt.axes([0.1, 0.55, 0.8, 0.05])

a_slider = Slider(slider_a, 'a', a_min, a_max, valinit=a_init)
b_slider = Slider(slider_b, 'b', a_min, a_max, valinit=a_init)
c_slider = Slider(slider_c, 'c', a_min, a_max, valinit=a_init)
d_slider = Slider(slider_d, 'd', a_min, a_max, valinit=a_init)
e_slider = Slider(slider_e, 'e', a_min, a_max, valinit=a_init)
f_slider = Slider(slider_f, 'f', a_min, a_max, valinit=a_init)

a, b, c, d, e, f = 0, 0, 0, 0, 0, 0


def update_ha(h):
    global a
    a = int(h)
    parameters.pink = ((min(a, d), min(b, e), min(c, f)), (max(a, d), max(b, e), max(c, f)))


def update_hb(h):
    global b
    b = int(h)
    parameters.pink = ((min(a, d), min(b, e), min(c, f)), (max(a, d), max(b, e), max(c, f)))


def update_sc(s):
    global c
    c = int(s)
    parameters.pink = ((min(a, d), min(b, e), min(c, f)), (max(a, d), max(b, e), max(c, f)))


def update_sd(s):
    global d
    d = int(s)
    parameters.pink = ((min(a, d), min(b, e), min(c, f)), (max(a, d), max(b, e), max(c, f)))


def update_ve(v):
    global e
    e = int(v)
    parameters.pink = ((min(a, d), min(b, e), min(c, f)), (max(a, d), max(b, e), max(c, f)))


def update_vf(v):
    global f
    f = int(v)
    parameters.pink = ((min(a, d), min(b, e), min(c, f)), (max(a, d), max(b, e), max(c, f)))


a_slider.on_changed(update_ha)
b_slider.on_changed(update_hb)
c_slider.on_changed(update_sc)
d_slider.on_changed(update_sd)
e_slider.on_changed(update_ve)
f_slider.on_changed(update_vf)


def target():
    vision = Vision()
    nav_system = NavSystem()
    try:
        nav_system.start()
        while True:
            dist, camera_to_ball_angle = vision.dist_angle_to_ball()
            nav_system.update_ball_pos(dist, camera_to_ball_angle)
    
    except KeyboardInterrupt:
        pass
    finally:
        nav_system.stop()
        vision.stop()
        raspi.stop()


thread = Thread(target=target)
thread.daemon = True
thread.start()
print('ayyyyyy lmao')
plt.show()
