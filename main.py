from vision_controller import VisionController
from position_system import PositionSystem
from drive_system import DriveSystem
import pigpio


screenwidth = (320, 240)
pi = pigpio.pi()
v = VisionController(screenwidth)
# d = DriveSystem(pi, 26, 13, 6, 5)
p = PositionSystem(pi, 18)


def vision_callback(x, diameter, sw):
    # p.adjust_servo(x, sw)
    p.queue_camera_data(x, diameter, sw)


# def get_next_target():
#     if p.has_next_target():
#         p.next_target()


v.set_callback(vision_callback)

try:
    v.loop()
except KeyboardInterrupt:
    print('im dead')
finally:
    print('stopping')
    # d.stop()
