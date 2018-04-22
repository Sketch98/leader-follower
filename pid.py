class PID:
    """It's a pid controller implementation that can be reset."""
    def __init__(self, pid_constants):
        self._kp = pid_constants['kp']
        self._ki = pid_constants['ki']
        self._kd = pid_constants['kd']
        self._integrator = 0
        self._last_error = 0
        self._dead_band = 0
        if 'dead_band' in pid_constants:
            self._dead_band = pid_constants['dead_band']
    
    def calc(self, error, time_elapsed):
        # proportional
        pid = self._kp*error
        
        # integral
        # use average of error and last error for trapezoid approximation
        self._integrator += time_elapsed*(error + self._last_error)/2
        pid += self._ki*self._integrator
        
        # differential
        pid += self._kd*(error - self._last_error)/time_elapsed
        self._last_error = error
        
        if abs(error) < self._dead_band:
            return 0.0
        return pid
    
    def reset(self):
        self._integrator = 0
        self._last_error = 0
