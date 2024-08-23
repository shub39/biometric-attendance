# File for the oled display

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from time import sleep
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106

# OLED display stuff

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, rotate=0)

def draw(mylist):
	index = 0
	with canvas(device) as draw:
		for item in mylist:
			draw.text((0, index), item, fill="white")
			index += 10

