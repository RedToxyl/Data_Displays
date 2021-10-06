import paho.mqtt.client as mqtt
import time
import json

# get data
# establish connection / logger

# main loop
# handle connection errors

# stuffloop
# is new timebloc
# -> send new datablocs
# check responses?
# room has problem?
# check for keyboardinterrupt
# -> open menu


# Definitions
DATAPATH = "/Users/thomaswolf/Desktop/Seminararbeit/Data_Displays/Helpfuls/ExamplePlan.json"
BROKER = "192.168.178.45"
CLIENTID = "ddisp_Controller"
TIMES = []

statuslist = []
currenttimebloc = None
newcurrenttimebloc = None

specials = []
timed_specials = []
toberemoved = []  # this only exist to now remove elements of a list that is beeing iterated through
specialid = 1

# TODO add graceful exit after the day is over


# menu function and functions for menu use
def menu():
	command = ""
	while command not in ["q", "s", "e", "c"]:
		command = input("This is the menu. What do you wish to do?\n(q)uit the program, (s)end a special message, (e)nd a special message, or (c)ontinue?    ")

	if command == "q":
		c_quit()
	elif command == "s":
		c_send_special()
	elif command == "e":
		try:
			doomed_specialint = (input("Which special do you want to end?:    "))
			c_end_special(doomed_specialint)
		except TypeError:
			print("This is not a valid id.")


def c_quit():
	quit()


# TODO implement special handling in Controller
def c_send_special():
	# gets the rooms this special should be send to
	special_rooms = []
	wanted = input("Enter desired special rooms 'A204,A207,C5,C8' or type 'ALL':    ")
	if wanted == "ALL":
		special_rooms = "ALL"
	else:
		for wr in wanted.split(","):
			special_rooms.append(wr)

	# gets message priority
	priority = int(input("Please choose a priority, 0>1>2:    "))

	# gets content
	# TODO set max char limit (also do that in ddisp_draw)
	content = input("What do you want the message to say?:    ")

	# assigns id
	global specialid
	number = specialid
	specialid += 1

	print(f"The id for this special message is:  {number}")

	# gets deletion method
	dm = ""
	while dm not in ("t", "m", "s"):
		dm = input("Do you want this to last until a certain time, last until you cancel it or just stop after an hour? Enter (t)ime, (m)anual, (s)tandard:    ")
	if dm == "t":
		# TODO input validation - everything just crashes if you mistype :)
		# TODO also dont add specials after 11pm
		timed_specials.append((number, input("Enter the time you wish (hh:mm):    ")))
	elif dm == "s":
		timed_specials.append((number, int(time.strftime("%H", time.localtime())) + 1))

	specials.append(number)

	message = {"NUMBER": f"{number}", "PRIORITY": f"{priority}", "TEXT": f"{content}", "IMAGE": "None"}
	message = f"{message}"

	if special_rooms == "ALL":
		client.publish("Main/Special/", message, 1, retain=False)
	else:
		for rm in special_rooms:
			client.publish(f"Main/Special/{rm}", message, 1, retain=False)


def c_end_special(number):

	# removes this from specials
	for spc in specials:
		if spc == number:
			specials.remove(spc)
			break
	# and from timed specials
	for spc in timed_specials:
		if spc[0] == number:
			timed_specials.remove(spc)
			break

	client.publish("Main/Cancel/", f"{number}", 1, retain=False)


# TODO define Callbacks
def on_connect(self, userdata, flags, rc):
	print("Connected with result code " + str(rc))


# Subscribing in on_connect() means that if we lose the connection and
# reconnect then subscriptions will be renewed.


# The callback for when a PUBLISH message is received from the server.
def on_message(self, userdata, msg):
	# adds a nonow status to the list of status reports
	if msg.topic.split("/")[1] == "Status":
		statuslist.append((msg.topic.split("/")[2], "NONOW"))


def on_disconnect(self, userdata, rc):
	if rc == 0:
		print(f"{self._client_id.decode('utf-8')} has disconnectet in an orderly fashion.")
		quit()
	else:
		print(f"{self._client_id.decode('utf-8')} has disconnected without grace.")
		quit()


# TODO define normal functions


def send_blocdata(kind, room, timebloc, teacher=None, clss=None, subject=None):
	if kind == "L":
		messagedata = {"TEACHER": f"{teacher}", "SUBJECT": f"{subject}", "CLASS": f"{clss}", "BLOCTIME": f"{timebloc}", "ROOM": f"{room}"}
	else:
		messagedata = {"TEACHER": "PAUSE", "SUBJECT": "None", "CLASS": "None", "BLOCTIME": f"{timebloc}", "ROOM": f"{room}"}

	message = f'{messagedata}'
	client.publish(f"Main/Data/{room}", message, 1, retain=False)
	client.loop()


# gets the data in a json file
raw_data = open(DATAPATH)
data = json.load(raw_data)

# stores the starts of timeblocs in a list for easy access
for bloc in data:
	TIMES.append(data[bloc]['TIME'].split("-")[0])

while True:
	try:
		# TODO connection
		# TODO stop this from happening every time I open the menu
		client = mqtt.Client(client_id=CLIENTID, clean_session=False)
		client.on_connect = on_connect
		client.on_message = on_message
		client.on_disconnect = on_disconnect

		client.connect(BROKER, 1883, 60)
		time.sleep(2)

		client.subscribe("Main/Status/#")
		try:

			while True:
				# gets time
				hour = int(time.strftime("%H", time.localtime()))
				minute = int(time.strftime("%M", time.localtime()))

				# checks whether there are specials that have ended
				for spec in timed_specials:
					if hour > int(spec[1].split(":")[0]):
						toberemoved.append(spec[0])
					elif hour == int(spec[1].split(":")[0]) and minute > int(spec[1].split(":")[1]):
						toberemoved.append(spec[0])

				# cancels ended timed specials
				for spec in toberemoved:
					c_end_special(spec[0])

				toberemoved = []

				# for every timebloc it checks whether the current our and minute are bigger, if yes, this is the current one now
				for timebloc in TIMES:
					if hour > int(timebloc.split(":")[0]):
						newcurrenttimebloc = TIMES.index(timebloc)
					elif hour == int(timebloc.split(":")[0]) and minute > int(timebloc.split(":")[1]):
						newcurrenttimebloc = TIMES.index(timebloc)

				# if the current timebloc is outdated, send all messages to each bloc
				if newcurrenttimebloc != currenttimebloc:
					currenttimebloc = newcurrenttimebloc

					# if not recess but lesson, send detailed blocdata
					if data[f"Bloc{currenttimebloc}"]["KIND"] == "L":
						# for every room, send data
						for room in data[f"Bloc{currenttimebloc}"]["ROOMGRID"]:
							send_blocdata(data[f"Bloc{currenttimebloc}"]["KIND"], room, data[f"Bloc{currenttimebloc}"]["TIME"], data[f"Bloc{currenttimebloc}"]["ROOMGRID"][f"{room}"]["TEACHER"], data[f"Bloc{currenttimebloc}"]["ROOMGRID"][f"{room}"]
							["CLASS"], data[f"Bloc{currenttimebloc}"]["ROOMGRID"][f"{room}"]["SUBJECT"])
					# TODO fix recess problems
					else:
						for room in data[f"Bloc{currenttimebloc}"]["ROOMGRID"]:
							send_blocdata(data[f"Bloc{currenttimebloc}"]["KIND"], room, data[f"Bloc{currenttimebloc}"]["TIME"])

					# do the same thing for the next bloc
					try:
						if data[f"Bloc{currenttimebloc + 1}"]["KIND"] == "L":
							for room in data[f"Bloc{currenttimebloc + 1}"]["ROOMGRID"]:
								send_blocdata(data[f"Bloc{currenttimebloc + 1}"]["KIND"], room, data[f"Bloc{currenttimebloc + 1}"]["TIME"], data[f"Bloc{currenttimebloc + 1}"]["ROOMGRID"][f"{room}"]["TEACHER"], data[f"Bloc{currenttimebloc + 1}"]
								["ROOMGRID"][f"{room}"]["CLASS"], data[f"Bloc{currenttimebloc + 1}"]["ROOMGRID"][f"{room}"]["SUBJECT"])

						else:
							for room in data[f"Bloc{currenttimebloc + 1}"]["ROOMGRID"]:
								send_blocdata(data[f"Bloc{currenttimebloc + 1}"]["KIND"], room, data[f"Bloc{currenttimebloc + 1}"]["TIME"])
					except ValueError:
						pass

				client.loop()

		except KeyboardInterrupt:
			# open menu
			menu()
	# TODO only except ddisp exception
	except IndentationError:
		# try to reconnect
		pass
