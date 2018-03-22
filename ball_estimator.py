from math import sin, cos, tan, asin, pi


def get_ball_angle(x_pix, screenwidth):
    camera_to_ball_angle = 180/pi*asin(0.8643*(x_pix/screenwidth - 0.5))
    print('camera-to-ball angle {}'.format(camera_to_ball_angle))
    # print('')
    return camera_to_ball_angle


def calc_ball_coordinates(servo_angle, x_pix, diameter, screenwidth):
    left_angle = asin(0.8643*((x_pix - diameter/2.0)/screenwidth - 0.5))
    right_angle = asin(0.8643*((x_pix + diameter/2.0)/screenwidth - 0.5))
    camera_to_ball_angle = 180/pi*(right_angle + left_angle)/2
    ball_angle = servo_angle - 90 + camera_to_ball_angle
    dist = abs(1.33/tan((right_angle-left_angle)/2.0))
    x = dist*sin(ball_angle*pi/180)
    y = dist*cos(ball_angle*pi/180)
    print('x_pos {}   y_pos {}   dist {}   servo_angle {}'.format(x, y, dist, servo_angle))
    print('left_angle {} right_angle {}   ball_angle {}'.format(180/pi*left_angle, 180/pi*right_angle, ball_angle))
    print('')
    
    return x, y, camera_to_ball_angle
