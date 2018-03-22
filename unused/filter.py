class Filter:
    def __init__(self):
        self.coefficients = [-3, 12, 17, 12, -3]
        self.buffer = [0.0, 0.0, 0.0, 0.0, 0.0]
    
    def queue(self, val):
        for i in range(len(self.buffer) - 1):
            self.buffer[i] = self.buffer[i+1]
        self.buffer[-1] = val
    
    def weighted_avg(self):
        avg = 0.0
        normalizing_factor = 0.0
        for i in range(len(self.buffer)):
            avg += self.buffer[i]*self.coefficients[i]
            normalizing_factor += self.coefficients[i]
        return avg/normalizing_factor
