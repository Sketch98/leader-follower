import pigpio

from nav_system import NavSystem
from position_system import PositionSystem
from vision import Vision

raspi = pigpio.pi()
v = Vision()
n = NavSystem(raspi)
p = PositionSystem(raspi, n)

try:
    n.start()
    v.loop(p.do_shit)
except KeyboardInterrupt:
    n.stop()
    v.stop()
    p.stop()
