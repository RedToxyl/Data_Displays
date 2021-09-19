import paho.mqtt.client as mqtt
import datetime


def on_message(self, userdata, msg):
	output = f"{msg.topic}:   {msg.payload.decode('utf-8')}"
	if "New connection" in output and "192.168.178." not in output:
		print("Warning! A user from a different Network has connected!\n")
	print(output)
	log = open(logid, "a")
	log.write(output + "\n")


def on_connect(self, userdata, flags, rc):
	print(f"Connection: {rc}")
	self.subscribe("$SYS/broker/log/#")


def on_disconnect(self, userdata, rc):
	print("Mosquitto shut down.")
	quit()


def makelog():
	global logid
	logid = f"/Users/thomaswolf/Desktop/Seminararbeit/Seminarcode/Datasharing/Mosquitto_Logs/{datetime.datetime.now().strftime('Log_%Y-%m-%d--%H-%M-%S')}.txt"
	print(logid)

makelog()
client = mqtt.Client("Logger")
client.on_message = on_message
client.on_connect = on_connect
client.on_disconnect = on_disconnect

client.connect("192.168.178.45")

client.loop_forever()
