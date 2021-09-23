def init_draw(width, height):
	# imports the necessary modules
	import Adafruit_SSD1306
	from PIL import Image
	from PIL import ImageDraw
	from PIL import ImageFont

	global WIDTH, HEIGHT, img, draw, font, disp
	WIDTH = width
	HEIGHT = height

	if WIDTH == 128 and HEIGHT == 64:
		# TODO what is rst? rename disp?
		disp = Adafruit_SSD1306.SSD1306_128_64(rst=None)
	else:
		# TODO create proper error
		raise KeyError

	# TODO draw opening sequences
	disp.begin()
	disp.clear()
	disp.display()

	img = Image.new("1", (WIDTH, HEIGHT))
	draw = ImageDraw.Draw(img)
	font = ImageFont.load_default()


def show_bloc(clss, subject, teacher, timebloc, room):

	# drawing new text
	draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)  # clears display
	draw.text((3, 3), f"{clss} - {subject}", 255, font)  # draws class and subject
	draw.text((int(input()), int(input()), f"{teacher}", 255, font))  # draws teacher
	#  draws room square
	#  draws room number
	draw.text((int(input()), int(input()), f"{timebloc}", 255, font))  # draws time

	disp.image(img)
	disp.display()
