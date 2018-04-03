import pigpio

from mcp3008 import MCP3008
from nav_system import NavSystem
from position_system import PositionSystem
from vision import Vision

raspi = pigpio.pi()
mcp = MCP3008()
vision = Vision()
nav_system = NavSystem()
position_system = PositionSystem()

try:
    nav_system.start()
    vision.loop(position_system.do_stuff)
except KeyboardInterrupt:
    nav_system.stop()
    vision.stop()
    position_system.stop()
