from mcp3008 import read_channel
from parameters import current_coefficient, current_time_limit


class CurrentSensor:
    def __init__(self, mcp_channel):
        self._mcp_channel = mcp_channel
        self._counter = 0
    
    def check_current(self):
        # convert adc reading to amps
        current = read_channel(self._mcp_channel)*current_coefficient
        if current >= 10:
            self._counter += 1
            if self._counter >= current_time_limit:
                return True
        else:
            self._counter = 0
        return False
