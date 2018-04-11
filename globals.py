from math import pi
import pigpio

raspi = pigpio.pi()


def limit(val, lower_limit, upper_limit):
    # stops val from exceeding set limits
    return min(max(val, lower_limit), upper_limit)


def symmetric_limit(val, upper_limit):
    return limit(val, -upper_limit, upper_limit)


def correct_angle(angle):
    while angle < -pi:
        angle += pi*2
    while angle > pi:
        angle -= pi*2
    return angle
