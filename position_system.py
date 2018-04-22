from filter import IrregularDoubleExponentialFilter
from parameters import ball_speed_smoothing_factors, ball_heading_smoothing_factors
from position import ZERO_POS


class PositionSystem:
    """Was planned to be used for tracking the absolute position of the ball in
    the navigation thread but I didn't have time to finish implementing the whole
    system before the expo."""
    
    def __init__(self):
        self._speed_filter = IrregularDoubleExponentialFilter(*ball_speed_smoothing_factors)
        self._heading_filter = IrregularDoubleExponentialFilter(*ball_heading_smoothing_factors)
        self.last_ball_loc = ZERO_POS
    
    def calc_ball_movement(self, dist_to_ball, angle_to_ball, vehicle_xy_theta,
                           time_elapsed):
        # calculate xy dif from vehicle
        rel_ball_pos_from_robot_pov = ZERO_POS.pos_from_dist_angle(dist_to_ball, angle_to_ball)
        
        # rotate rel xy offset then add to vehicle_pos to find the ball's
        # absolute position
        vehicle_pos, vehicle_theta = vehicle_xy_theta
        abs_ball_pos = vehicle_pos.pos_from_xy_angle_dif(rel_ball_pos_from_robot_pov,
                                                         vehicle_theta)
        
        # find dist and angle of ball from ball's last position
        ball_move_dist, ball_heading = \
            self.last_ball_loc.relative_dist_angle_to(abs_ball_pos)
        self.last_ball_loc = abs_ball_pos
        
        ball_speed = self._speed_filter.filter(ball_move_dist/time_elapsed, time_elapsed)
        ball_heading = self._heading_filter.filter(ball_heading, time_elapsed)
        
        # find the relative position of the vehicle from the ball's pov
        rel_robot_pos_from_ball_pov = ZERO_POS.pos_from_dist_angle(dist_to_ball,
                                                                   angle_to_ball -
                                                                   ball_heading)
        return rel_robot_pos_from_ball_pov, ball_heading, ball_speed
    
    def reset(self):
        self.last_ball_loc = ZERO_POS
