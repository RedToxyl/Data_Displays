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
	draw.text((int(input("a: ")), int(input("b: "))), "9A - Englisch", 255, font)
	draw.text((WIDTH / 2, HEIGHT / 2), "Grabow", 255, font)

	disp.image(img)
	disp.display()
	time.sleep(.1)