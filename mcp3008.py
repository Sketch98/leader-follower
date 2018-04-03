import Adafruit_GPIO.SPI as spi
import Adafruit_MCP3008


class MCP3008:
    instantiated = False
    
    def __init__(self):
        assert not MCP3008.instantiated, 'can only create one mcp3008'
        MCP3008.instantiated = True
        self._mcp = Adafruit_MCP3008.MCP3008(spi=spi.SpiDev(0, 0))
    
    def read_channel(self, channel):
        return self._mcp.read_adc(channel)
