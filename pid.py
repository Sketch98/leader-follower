class PID:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integrator = 0
        self.last_error = 0
    
    def calc(self, error):
        # proportional
        pid = self.kp*error
        
        # integral
        self.integrator += error
        pid += self.ki*self.integrator
        
        # differential
        pid += self.kd*(error - self.last_error)
        self.last_error = error
        
        return pid
    
    def reset(self):
        self.integrator = 0
        self.last_error = 0
