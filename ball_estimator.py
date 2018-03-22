from math import sqrt, sin, cos


def get_ball_angle(servo_angle, x_pix, screenwidth):
    return servo_angle + 26.75*(0.5 - x_pix/screenwidth)


def calc_ball_coordinates(servo_angle, x_pix, screenwidth, diameter):
    ball_angle = get_ball_angle(servo_angle, x_pix, screenwidth)
    d = 2.63*screenwidth/x_pix
    k = 1.325*(x_pix - screenwidth/2)/diameter
    h = sqrt(d*d + k*k)
    if k >= 0:
        x = h*cos(180-ball_angle)
        y = h*sin(180-ball_angle)
        return x, y
    else:
        x = h*sin(ball_angle-90)
        y = h*cos(ball_angle-90)
        return x, y
