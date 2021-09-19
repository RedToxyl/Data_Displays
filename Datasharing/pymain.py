import paho.mqtt.client as mqtt
import Adafruit_SSD1306
import PIL
import ast

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


print("GitTest")

# definitions
MAC = getmac()
ROOM = "A207"
CMDQUEUE = []


# Callback functions

def on_connect(client, userdata, flags, rc, properties=None):
	print("Connect_Response:  " + str(rc))


# when recieving a message, the client checks if it is a command or general data regarding the next time block.
# It also sorts the message into something general or concerning specifically itself. needed to process the data in the right way

def on_message(client, userdata, message):
	if "Main/Data" in message.topic:
		kind = ("specific", "data")
	elif "Main/Broadcast/Data" in message.topic:
		kind = ("general", "data")
	elif "Main/Command" in message.topic:
		kind = ("specific", "command")
	elif "Main/Broadcast/Command" in message.topic:
		kind = ("general", "command")
	else:
		kind = "unknown"

	content = ast.literal_eval(message.payload.decode('utf-8'))

	CMDQUEUE.append(Recieved(kind, content))


# simple data storage class
class Recieved:
	def __init__(self, kind, content):
		self.kind = kind
		self.content = content

	def __repr__(self):
		return self.kind, self.content


# a class storing information for the dataside of the display, this always has the same structure
class Dataside:
	def __init__(self, teacher=None, subject=None, clss=None, room=ROOM, time=None, next=False):
		self.teacher = teacher
		self.subject = subject
		self.clss = clss
		self.room = room
		self.time = time
		self.next = next

	def __repr__(self):
		return f"{self.teacher}, {self.subject}, {self.clss}, {self.room}, {self.time}"


if __name__ == "__main__":

	# client is created, client_id is the MAC Adress to prevent duplicate logins
	client = mqtt.Client(client_id=MAC, clean_session=False)

	# the various callback functions are assigned to the client, needed to execute them
	client.on_connect = on_connect
	client.on_message = on_message

	# the client connects to the broker
	client.connect("192.168.178.45", 1883, 60)

	# the client subscribes to commands, datasharing and the systemwide broadcasts
	client.subscribe(f"Main/Commands/{ROOM}")
	client.subscribe(f"Main/Data/{ROOM}")
	client.subscribe("Main/Broadcast/#")

	# setup adafruit
	# this initiates the dataside object, on which the normal info will be drawn
	dataside = Dataside()
	# boot sequence images

	while True:
		# Get commands
		client.loop_start()

		for msg in CMDQUEUE:

			# what happens if the input is meant for every client
			if msg.kind[0] == "general":

				# this is data concerning the timebloc, the datasides gets told that all following information regards the next bloc
				# the second thing is currently not implemented and might never be
				if msg.kind[1] == "data":
					dataside.time = msg.content["TIME"]
					if msg.content["TYPE"] == "R":
						dataside.next = True

				if msg.kind[1] == "command":
					pass

			# the input is only meant for one specific room
			if msg.kind[0] == "specific":
				# the dataside recieves the actual input for this specific room, class is called clss to avoid python keyword chicanery
				if msg.kind[1] == "data":
					dataside.teacher = msg.content["TEACHER"]
					dataside.subject = msg.content["SUBJECT"]
					dataside.clss = msg.content["CLASS"]
				if msg.kind[1] == "command":
					pass
		# fill the data side
		# fill the cmd side
		# return Status
		client.loop_stop()
		# switch displayed side if x seconds have passed since last switch
		# draw the side that needs to be displayed
		pass
