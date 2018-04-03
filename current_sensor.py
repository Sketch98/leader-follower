from parameters import current_coefficient, current_time_limit


class CurrentSensor:
    def __init__(self, mcp, channel):
        self.mcp = mcp
        self.channel = channel
        self.counter = 0
    
    def check_current(self):
        # convert adc reading to amps
        current = self.mcp.read_channel(self.channel)*current_coefficient
        if current >= 10:
            self.counter += 1
            if self.counter >= current_time_limit:
                return True
        else:
            self.counter = 0
        return False
