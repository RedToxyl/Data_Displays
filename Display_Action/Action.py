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
	# TODO get bigger font
	# bigfont = ImageFont.truetype()


def show_bloc(clss, subject, teacher, timebloc, room):

	# drawing new text
	draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)  # clears display
	draw.text((3, 3), f"{clss} - {subject}", 255, font)  # draws class and subject
	# thank you very much, I can't be bothered with this: https://stackoverflow.com/questions/1970807/center-middle-align-text-with-pil
	w, h = draw.textsize(teacher)
	draw.text(((WIDTH - w) / 2, (HEIGHT - h) / 2 - 10), f"{teacher}", 255, font)  # draws teacher
	draw.rectangle(((128 - int(HEIGHT / 3), 0), (128, 0 - int(HEIGHT / 3))), outline=255, fill=255)  # draws room square
	#  draws room number
	w, h = draw.textsize(timebloc)
	draw.text(((WIDTH - w) / 2, 40), f"{timebloc}", 255, )  # draws time

	disp.image(img)
	disp.display()

# TODO special blocs
# TODO special images


init_draw(128, 64)
show_bloc("9a", "Englisch", "Berg", "7:30 - 8:15", "214")