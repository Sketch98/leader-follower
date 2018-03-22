current_coefficient = 0.0488


class CurrentSensor:
    def __init__(self, mcp, channel, limit=80):
        self.mcp = mcp
        self.channel = channel
        self.counter = 0
        self.limit = limit
    
    def check_current(self):
        # convert adc reading to amps
        current = self.mcp.read_channel(self.channel)*current_coefficient
        if current >= 10:
            self.counter += 1
            if self.counter >= self.limit:
                return True
        else:
            self.counter = 0
        return False
