import time
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Definitions
WIDTH = 128
HEIGHT = 64

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=None)

# startup
disp.begin()

disp.clear()
disp.display()

img = Image.new("1", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(img)

font = ImageFont.load_default()

while True:
	if input() == "del":
		draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)
	draw.text((3, 3), "9A - Englisch", 255, font)
	draw.text((int(input()), int(input())), "Grabow", 255, font=font, align="center")

	disp.image(img)
	disp.display()
	time.sleep(1)