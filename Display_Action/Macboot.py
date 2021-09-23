import time
import Adafruit_SSD1306
from PIL import Image


whitescreen = Image.open("White.ppm").convert("1")
su1 = Image.open("su1.ppm").convert("1")
Apple = Image.open("Apple.ppm").convert("1")
Welcome = Image.open("Welcome.ppm").convert("1")
hello = Image.open("Hello2.pbm").convert("1")
cat = Image.open('happycat_oled_64.ppm').convert('1')


# Raspberry Pi pin configuration:
RST = None

# 128x64 display with hardware I2C:  #i might be imcompetent
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
while True:
	disp.clear()
	disp.display()

	disp.image(su1)
	disp.display()
	time.sleep(3)

	disp.image(whitescreen)
	disp.display()
	time.sleep(3)

	disp.image(Apple)
	disp.display()
	time.sleep(3)

	disp.image(Welcome)
	disp.display()
	time.sleep(5)

	disp.image(hello)
	disp.display()
	time.sleep(10)

	disp.image(cat)
	disp.display()
	time.sleep(10)

	disp.clear()
	disp.display()

	if input() == "quit":
		quit()