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


class ExponentialFilter():
    def __init__(self, smoothing_factor):
        assert 0 < smoothing_factor <= 1, 'smoothing factor must be in (0, ' \
                                          '1]. it is {}'.format(
            smoothing_factor)
        self._smoothing_factor = smoothing_factor
        self._smoothed = 0
    
    def filter(self, val):
        self._smoothed = self._smoothing_factor*val + (
                1 - self._smoothing_factor)*self._smoothed
        return self._smoothed
    
    def reset(self):
        self._smoothed = 0.0


class DoubleExponentialFilter():
    def __init__(self, smoothing_factor, trend_smoothing_factor):
        assert 0 < smoothing_factor <= 1, 'smoothing factor must be in (0, ' \
                                          '1]. it is {}'.format(
            smoothing_factor)
        self._smoothing_factor = smoothing_factor
        assert 0 < trend_smoothing_factor <= 1, 'trend smoothing factor must ' \
                                                'be in (0, 1]. it is {}'.format(
            trend_smoothing_factor)
        self._trend_smoothing_factor = trend_smoothing_factor
        self._smoothed = 0
        self._trend = 0
    
    def filter(self, val):
        last_value = self._trend
        self._smoothed = self._smoothing_factor*val + (
                1 - self._smoothing_factor)*(self._smoothed + self._trend)
        self._trend = self._trend_smoothing_factor*(self._smoothed -
                                                    last_value) \
                      + (
                              1 -
                              self._trend_smoothing_factor)*self._trend_smoothing_factor
        return self._smoothed
    
    def reset(self):
        self._smoothed = 0.0
        self._trend = 0.0
