import traceback

import paho.mqtt.client as mqtt
import ast
import time
import ddisp_draw

""" 

	Command Structure:

	incoming:
		Main/Command/Raspi_xyz
		Main/Data/Raspi_xyz
		Main/Broadcast/Data
		Main/Broadcast/Command

	outgoing:
		Main/Raspi_xyz/Status


	Example of an instruction:


	data = '{"TEACHER": "Berg", "SUBJECT": "Englisch", "CLASS": "10A", "BLOCTIME": "7:30-8:15"}'

	special = '{"NUMBER": "2", "PRIORITY": "1", "TEXT": "Hello World", "IMAGE": None}'

	cancel = '2'



"""


# functions relevant to the core functions

def getmac():
	macfile = open("/sys/class/net/eth0/address", "r")
	mac = macfile.read()
	mac = mac[0:-1]

	return mac


# definitions
MAC = getmac()
ROOM = "A207"  # different for all clients
BROKER = "192.168.178.45"  # needs to be defined for all clients
connection_flag = False  # flag regarding the client connection, used for connection error handling
specials = []
cmdqueue = []
now = None
after = None


class ddispException(Exception):
	def __init__(self, *args):
		if args:
			self.message = args[0]
		else:
			self.message = None

	def __repr__(self):
		if self.message:
			return self.message
		else:
			return "An unknown ddispException has occured."


class ddispCatastrophicException(ddispException):
	def __repr__(self):
		if self.message:
			return f"Catastrophic Error: {self.message}"
		else:
			return "An unknown catastrophic exception has occured."


# Callback functions

def on_connect(client, userdata, flags, rc, properties=None):
	if rc == 0:
		print("successful connection")
		global connection_flag
		connection_flag = True
	else:
		raise ddispException(f"The connection has failed. rc= {rc}")


def on_disconnect(client, userdata, rc):
	if rc == 1:
		print("disconnect successful")
	else:
		print(f"ERROR: Unexpected Connection Loss, rc='{rc}'")
		raise ddispException(f"Sudden Disconnect. rc= {rc}")


def on_message(client, userdata, message):
	# TODO MAYBE add standart specials
	# TODO deal with bad messages
	"""
			incoming messages can be one of three types

			Data is information about a standart timebloc and contains teacher, subject, class and it's time
			In order to allow for an easy display of the current and next bloc, ±now± will get
			automatically replaced by next and ±next± by the incoming message

			Special contains data about a special display, configured by the user on the broker
			New specials get added to the list specials, which gets sorted with ascending priority
			specials have an id to uniquely identify them
			special messages must always contain all keywords, though they can be empty

			Cancel messages consist solely out of a number
			When a cancel message arrives, all Specials with that id get removed from specials[]
	"""
	if message.topic.split("/")[1] == "Data":
		blocinfo = ast.literal_eval(message.payload.decode('utf-8'))
		global after, now
		now = after
		# TODO add try except here:
		after = Bloc(teacher=blocinfo['TEACHER'], subject=blocinfo['SUBJECT'], clss=blocinfo['CLASS'], bloctime=blocinfo['BLOCTIME'])

	elif message.topic.split("/")[1] == "Special":
		specinfo = ast.literal_eval(message.payload.decode('utf-8'))
		# TODO add try except here
		specials.append(Special(number=specinfo['NUMBER'], priority=specinfo['PRIORITY'], text=specinfo['TEXT'], img=specinfo['IMAGE']))

	elif message.topic.split("/")[1] == "Cancel":
		cancelled = int(message.payload.decode('utf-8'))
		for special in specials:
			if special.number == cancelled:
				specials.remove(special)


# dataclass for the bloc

class Bloc:
	def __init__(self, teacher=None, subject=None, clss=None, room=ROOM, bloctime=None):
		self.teacher = teacher
		self.subject = subject
		self.clss = clss
		self.room = room
		self.bloctime = bloctime

		if subject == "BREAK":
			self.recess = True
		else:
			self.recess = False

	def __repr__(self):
		return f"{self.teacher}, {self.subject}, {self.clss}, {self.room}, {self.bloctime}"


# dataclass for the special event

class Special:
	def __init__(self, number, text, img, priority=1):
		self.number = int(number)
		self.text = text
		self.img = img
		self.priority = int(priority)

	def __repr__(self):
		return f"id: {self.number}, prio: {self.priority}\n{self.text}"


if __name__ == "__main__":

	# client is created, client_id is the MAC Adress to prevent duplicate logins
	client = mqtt.Client(client_id=MAC, clean_session=False)

	# the various callback functions are assigned to the client
	client.on_connect = on_connect
	client.on_disconnect = on_disconnect
	client.on_message = on_message

	# client tries to connect to the broker
	try:
		client.connect(BROKER, 1883, 60)
		while not connection_flag:  # check for connection until on_connect has been called
			client.loop()
			time.sleep(2)
	except ddispException():  # in case of connection not working
		# TODO catastrophic connection error
		pass

	# TODO check for errors in subscription
	# the client subscribes to commands, datasharing and the systemwide broadcasts
	client.subscribe(f"Main/Cancel/{ROOM}")
	client.subscribe(f"Main/Special/{ROOM}")
	client.subscribe(f"Main/Data/{ROOM}")

	ddisp_draw.init_draw(128, 64)  # initialises the display for drawing
	# boot sequence images

	while True:
		# TODO normal error handling
		# connection
		# other
		try:
			while True:
				client.loop(timeout=2)  # checks for new messages
				# the following regulates with things are printed (displayed)
				specials.sort(key=lambda special: special.priority),  # the list of all special messages gets sorted by priority
				if specials:

					if specials[0].priority == 0:  # if the first special has priority 0 it will get both faces
						print(f"important Special: {specials[0]}")

					elif len(specials) > 1:  # if there are more than 1 specials, the two with the lowest priority will get shown
						print(f"First Special: {specials[0]}\nSecond Special: {specials[1]}")

					elif now:  # if there is only a special with priority > 0 and now exists, show both
						print(f"Special: {specials[0]}")
						time.sleep(5)
						ddisp_draw.show_bloc(now.clss, now.subject, now.teacher, now.bloctime, now.room)
						time.sleep(5)
					else:  # only a special exists
						print(f"Special: {specials[0]}")

				# none of this matters if there are no specials, in that case now and next will just rotate normally
				else:
					if now and after:
						ddisp_draw.show_bloc(now.clss, now.subject, now.teacher, now.bloctime, now.room)
						time.sleep(5)
						ddisp_draw.show_bloc(after.clss, after.subject, after.teacher, after.bloctime, after.room)
						time.sleep(5)
		# TODO status
		# return Status

		except ddispException:
			tries = 0
			while not connection_flag and tries < 5:
				client.reconnect()
				time.sleep(5)
			if not connection_flag:
				# TODO catastrophic connection error
				raise ddispCatastrophicException("Could not reconnect after 5 tries! Is the broker still online?")
				pass
		pass
