class PID:
    def __init__(self, kp, ki, kd, min_i, max_i, dead_zone=0.0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.min_i = min_i
        self.max_i = max_i
        self.dead_zone = dead_zone
        
        self.last_error = 0
        self.integrator = 0
        
        self.target = 0.0
    
    def calc(self, cur_val):
        error = self.target - cur_val
        
        # proportional
        ret = self.kp * error
        
        # integral
        self.integrator += error
        self.integrator = max(self.integrator, self.min_i)
        self.integrator = min(self.integrator, self.max_i)
        ret += self.ki * self.integrator
        
        # differential
        ret += self.kd * (error - self.last_error)
        self.last_error = error
        
        # zero output inside dead zone to avoid thrashing
        if abs(ret) < self.dead_zone:
            return 0.0
        return ret
    
    def set_target(self, target):
        self.target = target
