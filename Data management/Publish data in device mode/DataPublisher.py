import paho.mqtt.client as mqtt
from jsonDevData.LoSampleData import LoData, SampleData
from datetime import datetime
import numpy as np
import json
import time
#e6e10b0cdc50409bab7748f8c4d0dfd2
#Connection parameters
SERVER = "liveobjects.orange-business.com"
PORT = 1883
API_KEY   = "f5d08f4067e14db884b0d7ed6ea276a0"
USERNAME  = "json+device"
CLIENT_ID = "urn:lo:nsid:samples:TEST"

#Publications parameters
TOPIC="dev/data"
qos = 1


def on_connect(client, userdata, flags, rc):
    print("Connected in device mode with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(TOPIC)

# The callback for when a PUBLISH message is received from the server.
def on_message(sampleClient, userdata, msg):
    print(msg.topic+" "+str(msg.payload))



sampleClient = mqtt.Client(CLIENT_ID, clean_session=True, userdata = None, protocol=mqtt.MQTTv311, transport="tcp")
sampleClient.on_connect = on_connect
sampleClient.on_message = on_message
sampleClient.username_pw_set(USERNAME,password = list(API_KEY)) # use device mode and set the password
# now connect to LO
# while True:
sampleClient.connect(SERVER, PORT, 60)

# # create message
LoData = LoData()
myData = SampleData()

msgDt = datetime.now().isoformat()
LoData.s = "Stream1"
LoData.m = "samplesModel"
LoData.loc = np.array([48.125,2.185])
LoData.v = myData
myData.payload = "Message from deviceMode on dev/data on " + msgDt
myData.temperature=24
myData.hygrometry=12

msg = json.dumps(myData.__dict__) ## get all atributes values with .__dict__
sampleClient.loop_start()
sampleClient.publish(TOPIC, msg, qos)
print ("Message published")
print LoData.v
# time.sleep(3)

# Send your message

# Disconnect
sampleClient.disconnect()
print("Disconnected")
