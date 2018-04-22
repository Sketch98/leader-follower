from math import pi
import pigpio

raspi = pigpio.pi()


# stops val from exceeding set limits
def limit(val, lower_limit, upper_limit):
    return min(max(val, lower_limit), upper_limit)


# same thing as limit but in the case lower_limit = -upper_limit
def symmetric_limit(val, upper_limit):
    return limit(val, -upper_limit, upper_limit)


"""When representing angles with floats the possibility of the angle reaching
pi or -pi is present. This method rolls the angle around in those cases."""
def correct_angle(angle):
    while angle < -pi:
        angle += pi*2
    while angle > pi:
        angle -= pi*2
    return angle
