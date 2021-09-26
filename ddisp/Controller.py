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
		client = mqtt.Client(client_id=CLIENTID, clean_session=False)
		client.on_connect = on_connect
		client.on_message = on_message
		client.on_disconnect = on_disconnect

		client.connect(BROKER, 1883, 60)
		time.sleep(2)

		client.subscribe("Main/Status/#")
		try:

			while True:

				# for every timebloc it checks whether the current our and minute are bigger, if yes, this is the current one now
				for timebloc in TIMES:
					if int(time.strftime("%H", time.localtime())) > int(timebloc.split(":")[0]):
						newcurrenttimebloc = TIMES.index(timebloc)
					elif int(time.strftime("%H", time.localtime())) == int(timebloc.split(":")[0]) and int(time.strftime("%M", time.localtime())) > int(timebloc.split(":")[1]):
						newcurrenttimebloc = TIMES.index(timebloc)

				# if the current timebloc is outdated, send all messages to each bloc
				if newcurrenttimebloc != currenttimebloc:
					currenttimebloc = newcurrenttimebloc

					# if not a break, send detailed data
					if data[f"Bloc{currenttimebloc}"]["KIND"] == "L":
						for room in data[f"Bloc{currenttimebloc}"]["ROOMGRID"]:
							# TODO find way to send first one twice, perhaps via on message and status reports
							send_blocdata(data[f"Bloc{currenttimebloc}"]["KIND"], room, data[f"Bloc{currenttimebloc}"]["TIME"], data[f"Bloc{currenttimebloc}"]["ROOMGRID"][f"{room}"]["TEACHER"], data[f"Bloc{currenttimebloc}"]["ROOMGRID"][f"{room}"]["CLASS"], data[f"Bloc{currenttimebloc}"]["ROOMGRID"][f"{room}"]["SUBJECT"])
					# TODO fix recess problems
					else:
						for room in data[f"Bloc{currenttimebloc}"]["ROOMGRID"]:
							send_blocdata(data[f"Bloc{currenttimebloc}"]["KIND"], room, data[f"Bloc{currenttimebloc}"]["TIME"])

				# the status-handling
				# checks for statuses in the statuslist

				# in case of NONOW, send the current and the next info to the raspi in question
				for status in statuslist:
					if status[1] == "NONOW":
						send_blocdata(data[f"Bloc{currenttimebloc}"]["KIND"], status[0], data[f"Bloc{currenttimebloc}"]["TIME"], data[f"Bloc{currenttimebloc}"]["ROOMGRID"][f"{status[0]}"]["TEACHER"], data[f"Bloc{currenttimebloc}"]["ROOMGRID"]
						[f"{status[0]}"]["CLASS"], data[f"Bloc{currenttimebloc}"]["ROOMGRID"][f"{status[0]}"]["SUBJECT"])
						try:
							send_blocdata(data[f"Bloc{currenttimebloc + 1}"]["KIND"], status[0], data[f"Bloc{currenttimebloc + 1}"]["TIME"], data[f"Bloc{currenttimebloc + 1}"]["ROOMGRID"][f"{status[0]}"]["TEACHER"], data[f"Bloc{currenttimebloc + 1}"]
							["ROOMGRID"][f"{status[0]}"]["CLASS"], data[f"Bloc{currenttimebloc + 1}"]["ROOMGRID"][f"{status[0]}"]["SUBJECT"])
						except ValueError:
							send_blocdata(data[f"Bloc{currenttimebloc}"]["KIND"], status[0], data[f"Bloc{currenttimebloc}"]["TIME"], data[f"Bloc{currenttimebloc}"]["ROOMGRID"][f"{status[0]}"]["TEACHER"], data[f"Bloc{currenttimebloc}"]["ROOMGRID"]
							[f"{status[0]}"]["CLASS"], data[f"Bloc{currenttimebloc}"]["ROOMGRID"][f"{status[0]}"]["SUBJECT"])

				# reset statuslist after handling
				statuslist = []
				client.loop()

		except KeyboardInterrupt:
			# open menu
			if input("	Quit? (q)") == "q":
				quit()
	# TODO only except ddisp exception
	except IndentationError:
		# try to reconnect
		pass
