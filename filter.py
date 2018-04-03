class Filter:
    def __init__(self, coefficients):
        self._coefficients = coefficients
        self._buffer = [0]*len(coefficients)
    
    def queue(self, val):
        for i in range(len(self._buffer) - 1):
            self._buffer[i] = self._buffer[i + 1]
        self._buffer[-1] = val
        return self._weighted_avg()
    
    def _weighted_avg(self):
        avg = 0.0
        normalizing_factor = 0.0
        for i in range(len(self._buffer)):
            avg += self._buffer[i]*self._coefficients[i]
            normalizing_factor += self._coefficients[i]
        return avg/normalizing_factor
