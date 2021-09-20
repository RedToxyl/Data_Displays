import paho.mqtt.client as mqtt
import Adafruit_SSD1306
import PIL
import ast
import time

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

	
	msg = {image:"Hello2.ppm", text:"", custom:"", priority:"0"}}
	
	msg = {image:"", text:"Linus Schreiber, bitte ins Sekretariat kommen!", custom:"", priority:"0"}}
	
	msg = {image:"", text:"", custom:"...", priority:"0"}}
	
	Idea for a Slot-Structure
	
	messages have the format of (kind, content)
	
	kind is either data or command
	
	

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
COMMON_EXCEPTIONS = ()
SPECIAL = []
ERRORS = []
CMDQUEUE = []
CURRENT = None
NEXT = None


# TODO fix exceptions
class CustomException(Exception):
	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return self.name


ddisp_1 = CustomException("conniss")  # connection issue
ddisp_2 = CustomException("subiss")  # subscription issue


# Callback functions

def on_connect(client, userdata, flags, rc, properties=None):
	if rc == 0:
		print("successful connection")
		global connection_flag
		connection_flag = True
	else:
		print("connection failed")
		raise ddisp_1


def on_disconnect(client, userdata, rc):
	if rc == 1:
		print("disconnect successful")
	else:
		print(f"ERROR: Unexpected Connection Loss, rc='{rc}'")
		raise ddisp_1


def on_message(client, userdata, message):
	print(message.topic.split("/")[1])
	print(type(message.topic.split("/")[1]))
	if message.topic.split("/")[1] == 'Data':
		print("wtf")
	if message.topic.split("/")[1] == "Data":
		blocinfo = ast.literal_eval(message.payload.decode('utf-8'))
		global NEXT, CURRENT
		CURRENT = NEXT
		# TODO add try except here:
		NEXT = Bloc(teacher=blocinfo["TEACHER"], subject=blocinfo["SUBJECT"], clss=blocinfo["CLASS"], bloctime=blocinfo["BLOCTIME"], room=blocinfo["ROOM"])


# dataclass for the bloc

class Bloc:
	def __init__(self, teacher=None, subject=None, clss=None, room=None, bloctime=None):
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
	except ddisp_1:  # in case of connection not working
		# TODO catastrophic connection error
		pass

	# TODO check for errors in subscription
	# the client subscribes to commands, datasharing and the systemwide broadcasts
	client.subscribe(f"Main/Special/{ROOM}")
	client.subscribe(f"Main/Data/{ROOM}")

	# setup adafruit
	# boot sequence images

	while True:
		# TODO normal error handling
		# TODO connection error handling
		# connection
		# other
		try:
			while True:
				# TODO gather updates
				client.loop()

				# remove x from QUEUE
				if SPECIAL:
					# TODO special handling
					# draw special
					pass
				else:
					print(f"Now:    {CURRENT}")
					print(f"Next:    {NEXT}")
					# TODO drawing
					# draw face 1
					# wait 5
					# draw face 2
					pass
		# TODO status
		# return Status

		# TODO THIS IS A WORKAROUND (catch all exceptions)
		except:
			tries = 0
			while not connection_flag and tries < 5:
				client.reconnect()
				time.sleep(5)
			if not connection_flag:
				# TODO catastrophic connection error
				pass
		pass
