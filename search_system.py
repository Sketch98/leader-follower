from enum import Enum
from math import pi

from parameters import acceptable_angle_error, count_before_search, \
    spin_speed, \
    sweep_speed, sweeps_before_spin


class SearchMode(Enum):
    left = 'left'
    right = 'right'
    center = 'center'
    spin = 'spin'


target_angle = {
    SearchMode.left: -pi/2,
    SearchMode.right: pi/2,
    SearchMode.center: 0,
    SearchMode.spin: 0
}


class SearchSystem():
    
    def __init__(self):
        self._count = 0
        self._search_count = 0
        self._searching = False
        self._mode = SearchMode.left
        self._last_seen_angle = 0
        self._num_sweeps = 0
    
    def in_search_mode_simple(self, ball_angle):
        # ball_angle is None when the ball isn't on screen, so we need to
        # search for it
        if ball_angle is None:
            # set direction to angle of last seen direction if we're entering
            #  search mode
            # otherwise we don't want to modify direction because it needs to
            #  sweep back and forth
            # which requires it to be modified elsewhere
            if not self._searching:
                self._num_sweeps = 0
                self._mode = SearchMode.left if self._last_seen_angle < 0 \
                    else SearchMode.right
                self._searching = True
        else:
            self._last_seen_angle = ball_angle
            self._searching = False
        return self._searching
    
    def in_search_mode(self, ball_angle):
        # ball_angle is None when the ball isn't on screen, so we need to
        # search for it
        if ball_angle is None:
            if self._searching:
                return True
            self._count += 1
        else:
            self._last_seen_angle = ball_angle
            self._count = max(self._count - 2, 0)
            self._searching = False
        
        # enter search mode if reached count_before_search
        if self._count == count_before_search:
            self._mode = SearchMode.left if self._last_seen_angle < 0 else \
                SearchMode.right
            self._searching = True
        return self._searching
    
    def reached_target_angle(self, servo_angle):
        lower_bound = target_angle[self._mode] - acceptable_angle_error
        upper_bound = target_angle[self._mode] + acceptable_angle_error
        if lower_bound <= servo_angle <= upper_bound:
            self._num_sweeps += 1
            return True
        return False
    
    def search_servo(self, servo_angle):
        if self._mode == SearchMode.left:
            # check if reached destination
            if self.reached_target_angle(servo_angle):
                self._mode = SearchMode.right
                # switch to center if reached num_sweeps
                if self._num_sweeps >= sweeps_before_spin:
                    self._mode = SearchMode.center
                return self.search_servo(servo_angle)
            # sweep left (negative)
            return -sweep_speed
        
        elif self._mode == SearchMode.right:
            # check if reached destination
            if self.reached_target_angle(servo_angle):
                self._mode = SearchMode.left
                # switch to center if reached num_sweeps
                if self._num_sweeps >= sweeps_before_spin:
                    self._mode = SearchMode.center
                return self.search_servo(servo_angle)
            # sweep right (positive)
            return sweep_speed
        
        elif self._mode == SearchMode.center:
            if self.reached_target_angle(servo_angle):
                self._mode = SearchMode.spin
                return self.search_servo(servo_angle)
            # move servo to center (assume center is at 0 radians)
            return -servo_angle
        
        elif self._mode == SearchMode.spin:
            # keep servo in center then spin robot
            return -servo_angle
    
    def search_angular_speed(self):
        if self._mode == SearchMode.left:
            return 0.0
        elif self._mode == SearchMode.right:
            return 0.0
        elif self._mode == SearchMode.center:
            return 0.0
        elif self._mode == SearchMode.spin:
            return spin_speed
