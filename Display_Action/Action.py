def init_draw(width, height):
	# imports the necessary modules
	import Adafruit_SSD1306
	from PIL import Image
	from PIL import ImageDraw
	from PIL import ImageFont

	global WIDTH, HEIGHT, img, draw, font, disp, font, bigfont
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
	font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf")
	bigfont = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf", 15)


def show_bloc(clss, subject, teacher, timebloc, room):

	# drawing new text
	draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)  # clears display
	draw.text((3, 3), f"{clss} - {subject}", 255, font=font)  # draws class and subject

	# thank you very much, I can't be bothered with this: https://stackoverflow.com/questions/1970807/center-middle-align-text-with-pil
	w, h = draw.textsize(teacher)
	draw.text(((WIDTH - w) / 2, (HEIGHT - h) / 2 - 10), f"{teacher}", 255, font=font)  # draws teacher

	# draws room square
	x1 = WIDTH - int(HEIGHT / 3) - 15
	x2 = WIDTH
	y1 = 0
	y2 = int(HEIGHT / 3)
	draw.rectangle(((x1, y1), (x2, y2)), outline=255, fill=255)
	draw.text((x2 - (x2 - x1) / 2, (y2 - (y2 - y1) / 2)), text=f"{room}", fill=0, font=font, anchor="m")  # draws room number

	w, h = draw.textsize(timebloc)
	draw.text(((WIDTH - w) / 2, 40), f"{timebloc}", 255, font=bigfont)  # draws time

	disp.image(img)
	disp.display()

# TODO special blocs
# TODO special images


init_draw(128, 64)
show_bloc("9a", "Englisch", "Berg", "7:30 - 8:15", "214")