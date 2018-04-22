import time

import Adafruit_GPIO.SPI as spi
import Adafruit_MCP3008 as mcp3008


"""Tests the MCP3008 ADC."""


# Hardware SPI configuration:
SPI_PORT = 0
SPI_DEVICE = 0
mcp = mcp3008.MCP3008(spi=spi.SpiDev(SPI_PORT, SPI_DEVICE))

print('Reading MCP3008 values, press Ctrl-C to quit...')
# Main program loop.
while True:
    val = mcp.read_adc(0)
    # Print the ADC values.
    print('{}'.format(val))
    # Pause for half a second.
    time.sleep(0.5)
