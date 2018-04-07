import Adafruit_GPIO.SPI as spi
import Adafruit_MCP3008

mcp = Adafruit_MCP3008.MCP3008(spi=spi.SpiDev(0, 0))


def read_channel(channel):
    return mcp.read_adc(channel)
