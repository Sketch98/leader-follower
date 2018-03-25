class PIDController:
    def __init__(self, kp, ki, kd, dead_zone=0.0, limit_i=False, min_i=-1000.0, max_i=1000.0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        if limit_i:
            self.min_i = min_i
            self.max_i = max_i
        self.dead_zone = dead_zone
        self.limit_i = limit_i
        self.integrator = 0
        self.last_error = 0
    
    def calc(self, error):
        # proportional
        pid = self.kp * error
        
        # integral
        self.integrator += error
        if self.limit_i:
            self.integrator = min(self.max_i, max(self.integrator, self.min_i))
        pid += self.ki * self.integrator
        
        # differential
        pid += self.kd * (error - self.last_error)
        self.last_error = error
        
        # zero output inside dead zone to avoid thrashing
        if abs(pid) < self.dead_zone:
            return 0.0
        print(pid)
        return pid


class PIController:
    def __init__(self, kp, ki, dead_zone=0.0, limit_i=False, min_i=-1000.0, max_i=1000.0):
        self.kp = kp
        self.ki = ki
        if limit_i:
            self.min_i = min_i
            self.max_i = max_i
        self.dead_zone = dead_zone
        self.limit_i = limit_i
        self.integrator = 0
    
    def calc(self, error):
        # proportional
        # TODO: rename this
        pi = self.kp * error
        
        # integral
        self.integrator += error
        if self.limit_i:
            self.integrator = min(self.max_i, max(self.integrator, self.min_i))
        pi += self.ki * self.integrator
        
        # zero output inside dead zone to avoid thrashing
        if abs(pi) < self.dead_zone:
            return 0.0
        print(pi)
        return pi
