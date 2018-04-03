class PID:
    def __init__(self, pid_constants):
        self.kp = pid_constants['kp']
        self.ki = pid_constants['ki']
        self.kd = pid_constants['kd']
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
