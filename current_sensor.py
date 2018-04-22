from mcp3008 import read_channel
from parameters import current_time_limit


class CurrentException(Exception):
    pass


class CurrentSensor:
    """This class is supposed to interface with the MCP3008 ADC to measure the
    current the motors are pulling but all tests with this code yielded weird
    results such as the exception being raised immediately even when the motors
    aren't connected.
    
    For this reason the condition passes instead of raising the exception."""
    def __init__(self, mcp_channel):
        self._mcp_channel = mcp_channel
        self._count = 0
    
    def check_current(self):
        # convert adc reading to amps
        current = read_channel(self._mcp_channel)
        current = (current - 510)*3.3/1024/0.04 - 0.04
        if current >= 30:
            self._count += 1
            if self._count >= current_time_limit:
                pass
                # raise CurrentException
        else:
            self._count -= 1
