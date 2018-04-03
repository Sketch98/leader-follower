class PID:
    def __init__(self, pid_constants):
        self._kp = pid_constants['kp']
        self._ki = pid_constants['ki']
        self._kd = pid_constants['kd']
        self._integrator = 0
        self._last_error = 0
    
    def calc(self, error):
        # proportional
        pid = self._kp*error
        
        # integral
        self._integrator += error
        pid += self._ki*self._integrator
        
        # differential
        pid += self._kd*(error - self._last_error)
        self._last_error = error
        
        return pid
    
    def reset(self):
        self._integrator = 0
        self._last_error = 0
