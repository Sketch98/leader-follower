from math import atan2, cos, sin, sqrt


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def relative_xy_to(self, p):
        return Position(self.x - p.x, self.y - p.y)
    
    def relative_dist_angle_to(self, p):
        dif = self.relative_xy_to(p)
        dist = sqrt(dif.x*dif.x + dif.y*dif.y)
        angle = atan2(dif.y, dif.x)
        return dist, angle
    
    def pos_from_xy_dif(self, p):
        return Position(self.x + p.x, self.y + p.y)
    
    def pos_from_xy_angle_dif(self, dif, angle):
        x = self.x + dif.x*cos(angle) + dif.y*sin(angle)
        y = self.y - dif.x*sin(angle) + dif.y*cos(angle)
        return Position(x, y)
    
    def pos_from_dist_angle(self, dist, angle):
        x = self.x + dist*sin(angle)
        y = self.y + dist*cos(angle)
        return Position(x, y)


ZERO_POS = Position(0, 0)
