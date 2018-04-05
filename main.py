from globals import raspi

from nav_system import NavSystem
from position_system import PositionSystem
from vision import Vision

vision = Vision()
nav_system = NavSystem()
position_system = PositionSystem(nav_system)

try:
    nav_system.start()
    vision.loop(position_system.do_stuff)
except KeyboardInterrupt:
    nav_system.stop()
    vision.stop()
    position_system.stop()
    raspi.stop()
