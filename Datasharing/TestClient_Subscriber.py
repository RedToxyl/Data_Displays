import paho.mqtt.client as mqtt


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


client = mqtt.Client(client_id="TestClient_Subscriber", clean_session=False)
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect("192.168.178.45", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

client.loop_start()
client.subscribe("News/")
client.subscribe("Main/Data/")
client.subscribe("Main/Special/")
client.subscribe("Main/Status/")
client.loop_stop()

while True:
	client.loop()
