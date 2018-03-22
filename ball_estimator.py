from math import sin, cos, tan, asin, pi


def get_angle_to_pixel(x_pix, screenwidth):
    # corrects for camera's lens projecting curved light onto a flat sensor
    angle = asin(0.8643*(x_pix/screenwidth - 0.5))
    return angle


def calc_ball_coordinates(servo_angle, x_pix, diameter, screenwidth):
    """
    finds the angles to the left and right sides of the ball.
    it uses that to estimate the distance to the ball and the ball's relative xy position
    """
    left_angle = get_angle_to_pixel(x_pix - diameter / 2.0, screenwidth)
    right_angle = get_angle_to_pixel(x_pix + diameter / 2.0, screenwidth)
    camera_to_ball_angle = (right_angle + left_angle)/2
    ball_angle = servo_angle + camera_to_ball_angle
    dist = abs(33.1/tan((right_angle-left_angle)/2.0))
    x = dist*sin(ball_angle)
    y = dist*cos(ball_angle)
    print('x_pos {}   y_pos {}   dist {}   servo_angle {}'.format(x, y, dist, 180/pi*servo_angle))
    print('left_angle {} right_angle {}   ball_angle {}'.format(180/pi*left_angle, 180/pi*right_angle, 180/pi*ball_angle))
    print('')
    return x, y, camera_to_ball_angle
