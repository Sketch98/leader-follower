class PID:
    def __init__(self, kp, ki, kd, dead_zone=0.0, limit_i=False, min_i=1.0, max_i=-1.0):
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
        sum = self.kp * error
        
        # integral
        self.integrator += error
        if self.limit_i:
            self.integrator = min(self.max_i, max(self.integrator, self.min_i))
        sum += self.ki * self.integrator
        
        # differential
        sum += self.kd * (error - self.last_error)
        self.last_error = error
        
        # zero output inside dead zone to avoid thrashing
        if abs(sum) < self.dead_zone:
            return 0.0
        return sum
