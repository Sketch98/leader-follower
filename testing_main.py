from globals import raspi
from nav_system import NavSystem
from parameters import pink as default_pink
from parameters import awb_gains as default_awb_gains
from pi_video_stream import PiVideoStream

from matplotlib.widgets import Slider
import matplotlib.pyplot as plt


nav_system = NavSystem()


def pvs_callback(dist, camera_to_ball_angle):
    nav_system.update_ball_pos(dist, camera_to_ball_angle)


pvs = PiVideoStream(pvs_callback, display=True)

a_min = 0
a_max = 255
a_init = 0

slider_h0 = plt.axes([0.1, 0.55, 0.8, 0.05])
slider_h1 = plt.axes([0.1, 0.45, 0.8, 0.05])
slider_s0 = plt.axes([0.1, 0.35, 0.8, 0.05])
slider_s1 = plt.axes([0.1, 0.25, 0.8, 0.05])
slider_v0 = plt.axes([0.1, 0.15, 0.8, 0.05])
slider_v1 = plt.axes([0.1, 0.05, 0.8, 0.05])

h0_slider = Slider(slider_h0, 'h0', a_min, a_max, valinit=default_pink[0][0])
h1_slider = Slider(slider_h1, 'h1', a_min, a_max, valinit=default_pink[1][0])
s0_slider = Slider(slider_s0, 's0', a_min, a_max, valinit=default_pink[0][1])
s1_slider = Slider(slider_s1, 's1', a_min, a_max, valinit=default_pink[1][1])
v0_slider = Slider(slider_v0, 'v0', a_min, a_max, valinit=default_pink[0][2])
v1_slider = Slider(slider_v1, 'v1', a_min, a_max, valinit=default_pink[1][2])

h0, s0, v0 = default_pink[0]
h1, s1, v1 = default_pink[1]


def update_h0(h):
    global h0
    h0 = int(h)
    pvs.pink = ((min(h0, h1), min(s0, s1), min(v0, v1)), (max(h0, h1), max(s0, s1), max(v0, v1)))


def update_h1(h):
    global h1
    h1 = int(h)
    pvs.pink = ((min(h0, h1), min(s0, s1), min(v0, v1)), (max(h0, h1), max(s0, s1), max(v0, v1)))


def update_s0(s):
    global s0
    s0 = int(s)
    pvs.pink = ((min(h0, h1), min(s0, s1), min(v0, v1)), (max(h0, h1), max(s0, s1), max(v0, v1)))


def update_s1(s):
    global s1
    s1 = int(s)
    pvs.pink = ((min(h0, h1), min(s0, s1), min(v0, v1)), (max(h0, h1), max(s0, s1), max(v0, v1)))


def update_v0(v):
    global v0
    v0 = int(v)
    pvs.pink = ((min(h0, h1), min(s0, s1), min(v0, v1)), (max(h0, h1), max(s0, s1), max(v0, v1)))


def update_v1(v):
    global v1
    v1 = int(v)
    pvs.pink = ((min(h0, h1), min(s0, s1), min(v0, v1)), (max(h0, h1), max(s0, s1), max(v0, v1)))


h0_slider.on_changed(update_h0)
h1_slider.on_changed(update_h1)
s0_slider.on_changed(update_s0)
s1_slider.on_changed(update_s1)
v0_slider.on_changed(update_v0)
v1_slider.on_changed(update_v1)


slider_rg = plt.axes([0.1, 0.85, 0.8, 0.05])
slider_bg = plt.axes([0.1, 0.75, 0.8, 0.05])
slider_iso = plt.axes([0.1, 0.65, 0.8, 0.05])

rg_slider = Slider(slider_rg, 'rg', 0.0, 3.0, valinit=default_awb_gains[0])
bg_slider = Slider(slider_bg, 'bg', 0.0, 3.0, valinit=default_awb_gains[1])
iso_slider = Slider(slider_iso, 'iso', 0, 900, valinit=200)

rg, bg = default_awb_gains


def update_rg(a):
    global rg
    rg = a
    pvs.set_awb_gains((rg, bg))


def update_bg(a):
    global bg
    bg = a
    pvs.set_awb_gains((rg, bg))


def update_iso(iso):
    pvs.set_iso(iso)


rg_slider.on_changed(update_rg)
bg_slider.on_changed(update_bg)
iso_slider.on_changed(update_iso)


nav_system.start()
pvs.start()

plt.show()

pvs.stop()
nav_system.stop()
raspi.stop()
