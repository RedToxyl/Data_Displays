def init_draw(width, height):
	# imports the necessary modules
	import Adafruit_SSD1306
	from PIL import Image
	from PIL import ImageDraw
	from PIL import ImageFont

	global WIDTH, HEIGHT, img, draw, font, disp, font, bigfont, mediumfont
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
	mediumfont = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf", 12)
	bigfont = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf", 15)


def show_bloc(clss, subject, teacher, timebloc, room, nxt=False):
	# drawing new text
	draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)  # clears display

	# thank you so very very much, I can't be bothered with this: https://stackoverflow.com/questions/1970807/center-middle-align-text-with-pil
	w, h = draw.textsize(teacher, font=mediumfont)
	draw.text(((WIDTH - w) / 2, (HEIGHT - h) / 2), f"{teacher}", 255, font=mediumfont)  # draws teacher

	# draws class and subject
	draw.text((3, 3), f"{clss}-{subject}", 255, font=font)

	# TODO differentiate current and next bloc somehow
	# draw.text((3, 3), "Danach: ", 255, mediumfont)  # for the next bloc in line

	# points to create the roomrectangle
	x1 = WIDTH - int(HEIGHT / 3) - 15
	x2 = WIDTH
	y1 = 0
	y2 = int(HEIGHT / 3)

	if draw.textsize(f"{clss}-{subject}", font=mediumfont)[0] < WIDTH - (x2 - x1) - 3:  # if the size of the class and subject is smaller than the space without the room-rectangle and the left ofset (here 3), do not draw roomnumber
		overhang = True
	else:
		overhang = False

	if not overhang:
		# draws room square
		draw.rectangle(((x1, y1), (x2, y2)), outline=255, fill=255)

		# draws room number
		w, h = draw.textsize(room, font=mediumfont)
		draw.text((x2 - ((x2 - x1 - w) / 2) - w, y2 - ((y2 - y1 - h) / 2) - h), text=f"{room}", fill=0, font=mediumfont)

	# draws time
	w, h = draw.textsize(timebloc, font=bigfont)
	draw.text(((WIDTH - w) / 2, 50), f"{timebloc}", 255, font=bigfont)

	disp.image(img)
	disp.display()


def show_special(text):
	# TODO implement multiline text
	draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)
	draw.multiline_text((5, 5), text, 255, font)
	disp.image(img)
	disp.display()


def show_image(image):
	# TODO special images
	draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)
	disp.image(image)
	disp.display()