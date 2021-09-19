"""MQTT version 3.1/3.1.1/5.0 client class.

This is the main class for use communicating with an MQTT broker.

General usage flow:

* Use connect()/connect_async() to connect to a broker
* Call loop() frequently to maintain network traffic flow with the broker
* Or use loop_start() to set a thread running to call loop() for you.
* Or use loop_forever() to handle calling loop() for you in a blocking
* function.
* Use subscribe() to subscribe to a topic and receive messages
* Use publish() to send messages
* Use disconnect() to disconnect from the broker

Data returned from the broker is made available with the use of callback
functions as described below.

Callbacks
=========

A number of callback functions are available to receive data back from the
broker. To use a callback, define a function and then assign it to the
client:

def on_connect(client, userdata, flags, rc, properties=None):
    print("Connection returned " + str(rc))

client.on_connect = on_connect

All of the callbacks as described below have a "client" and an "userdata"
argument. "client" is the Client instance that is calling the callback.
"userdata" is user data of any type and can be set when creating a new client
instance or with user_data_set(userdata).

If you wish to suppress exceptions within a callback, you should set
`client.suppress_exceptions = True`

The callbacks:

on_connect(client, userdata, flags, rc, properties=None): called when the broker responds to our connection
  request.
  flags is a dict that contains response flags from the broker:
    flags['session present'] - this flag is useful for clients that are
        using clean session set to 0 only. If a client with clean
        session=0, that reconnects to a broker that it has previously
        connected to, this flag indicates whether the broker still has the
        session information for the client. If 1, the session still exists.
  The value of rc determines success or not:
    0: Connection successful
    1: Connection refused - incorrect protocol version
    2: Connection refused - invalid client identifier
    3: Connection refused - server unavailable
    4: Connection refused - bad username or password
    5: Connection refused - not authorised
    6-255: Currently unused.

on_disconnect(client, userdata, rc): called when the client disconnects from the broker.
  The rc parameter indicates the disconnection state. If MQTT_ERR_SUCCESS
  (0), the callback was called in response to a disconnect() call. If any
  other value the disconnection was unexpected, such as might be caused by
  a network error.

on_disconnect(client, userdata, rc, properties): called when the MQTT V5 client disconnects from the broker.
  When using MQTT V5, the broker can send a disconnect message to the client.  The
  message can contain a reason code and MQTT V5 properties.  The properties parameter could be
  None if they do not exist in the disconnect message.

on_message(client, userdata, message): called when a message has been received on a
  topic that the client subscribes to. The message variable is a
  MQTTMessage that describes all of the message parameters.

on_publish(client, userdata, mid): called when a message that was to be sent using the
  publish() call has completed transmission to the broker. For messages
  with QoS levels 1 and 2, this means that the appropriate handshakes have
  completed. For QoS 0, this simply means that the message has left the
  client. The mid variable matches the mid variable returned from the
  corresponding publish() call, to allow outgoing messages to be tracked.
  This callback is important because even if the publish() call returns
  success, it does not always mean that the message has been sent.

on_subscribe(client, userdata, mid, granted_qos, properties=None): called when the broker responds to a
  subscribe request. The mid variable matches the mid variable returned
  from the corresponding subscribe() call. The granted_qos variable is a
  list of integers that give the QoS level the broker has granted for each
  of the different subscription requests.

on_unsubscribe(client, userdata, mid): called when the broker responds to an unsubscribe
  request. The mid variable matches the mid variable returned from the
  corresponding unsubscribe() call.

on_log(client, userdata, level, buf): called when the client has log information. Define
  to allow debugging. The level variable gives the severity of the message
  and will be one of MQTT_LOG_INFO, MQTT_LOG_NOTICE, MQTT_LOG_WARNING,
  MQTT_LOG_ERR, and MQTT_LOG_DEBUG. The message itself is in buf.

on_socket_open(client, userdata, sock): Called when the socket has been opened. Use this
  to register the socket with an external event loop for reading.

on_socket_close(client, userdata, sock): Called when the socket is about to be closed.
  Use this to unregister a socket from an external event loop for reading.

on_socket_register_write(client, userdata, sock): Called when a write operation to the
  socket failed because it would have blocked, e.g. output buffer full. Use this to
  register the socket with an external event loop for writing.

on_socket_unregister_write(client, userdata, sock): Called when a write operation to the
  socket succeeded after it had previously failed. Use this to unregister the socket
  from an external event loop for writing.
"""