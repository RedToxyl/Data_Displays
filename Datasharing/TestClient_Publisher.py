import paho.mqtt.client as mqtt
import time


# The callback for when the client receives a CONNACK response from the server.
def on_connect(self, userdata, flags, rc):
	print("Connected with result code " + str(rc))


# Subscribing in on_connect() means that if we lose the connection and
# reconnect then subscriptions will be renewed.


# The callback for when a PUBLISH message is received from the server.
def on_message(self, userdata, msg):
	output = f"{msg.topic}:   {msg.payload.decode('utf-8')}"
	print(output)


def on_disconnect(self, userdata, rc):
	if rc == 0:
		print(f"{self._client_id.decode('utf-8')} has disconnectet in an orderly fashion.")
		quit()
	else:
		print(f"{self._client_id.decode('utf-8')} has disconnected without grace.")
		quit()


client = mqtt.Client(client_id="TestClient_Publisher", clean_session=False)
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect("192.168.178.45", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

mode = 0
while mode not in ["b", "m", "s"]:
	mode = input("Please enter mode. (b)loc, (m)anual, (s)pecial:    ")

if mode == "m":
	while True:
		client.loop_start()
		message = input("Enter message:    ")
		client.publish("News/", message, 1, retain=False)
		client.loop_stop()

if mode == "b":
	while True:
		client.loop_start()
		message = '{"TEACHER": "Berg", "SUBJECT": "Englisch", "CLASS": "10A", "BLOCTIME": "7:30-8:15", "ROOM": "207"}'
		input()
		client.publish("Main/Data/A207", message, 1, retain=False)
		client.loop_stop()

		client.loop_start()
		message = '{"TEACHER": "None", "SUBJECT": "BREAK", "CLASS": "None", "BLOCTIME": "8:15-8:30", "ROOM": "None"}'
		input()
		client.publish("Main/Data/A207", message, 1, retain=False)
		client.loop_stop()

		client.loop_start()
		message = '{"TEACHER": "Schiemenz", "SUBJECT": "Mathe", "CLASS": "LK1 12", "BLOCTIME": "8:30-9:15", "ROOM": "207"}'
		input()
		client.publish("Main/Data/A207", message, 1, retain=False)
		client.loop_stop()

if mode == "s":
	while True:
		client.loop_start()
		message = '{"TEACHER": "Berg", "SUBJECT": "Englisch", "CLASS": "10A", "BLOCTIME": "7:30-8:15", "ROOM": "207"}'
		input()
		client.publish("Main/Data/A207", message, 1, retain=False)
		client.loop_stop()

		client.loop_start()
		message = '{"TEACHER": "None", "SUBJECT": "BREAK", "CLASS": "None", "BLOCTIME": "8:15-8:30", "ROOM": "None"}'
		input()
		client.publish("Main/Data/A207", message, 1, retain=False)
		client.loop_stop()

		client.loop_start()
		message = '{"NUMBER": "2", "PRIORITY": "0", "TEXT": "Hello World", "IMAGE": None}'
		input()
		client.publish("Main/Special/A207", message, 1, retain=False)
		client.loop_stop()

		client.loop_start()
		message = '{"NUMBER": "3", "PRIORITY": "1", "TEXT": "prio1", "IMAGE": None}'
		input()
		client.publish("Main/Special/A207", message, 1, retain=False)
		client.loop_stop()

		client.loop_start()
		message = '2'
		input()
		client.publish("Main/Cancel/A207", message, 1, retain=False)
		client.loop_stop()

		client.loop_start()
		message = '3'
		input()
		client.publish("Main/Cancel/A207", message, 1, retain=False)
		client.loop_stop()

while True:
	client.loop_start()
	# message = input("Enter message:    ")
	# client.publish("News/", message, 1, retain=False)
	message = '{"TEACHER": "Berg", "SUBJECT": "Englisch", "CLASS": "10A"}'
	client.publish("Main/Data/A207", message, 1, retain=False)
	client.loop_stop()
	time.sleep(10)
