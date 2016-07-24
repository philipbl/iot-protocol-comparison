import argparse
import json
import time

import paho.mqtt.client as mqtt

parser = argparse.ArgumentParser(description='Create MQTT subscriber')
parser.add_argument('server')
parser.add_argument('--keep-alive', default=60)
parser.add_argument('--qos', default=0, type=int)

args = parser.parse_args()

server = args.server
keep_alive = args.keep_alive
qos = args.qos

def on_connect(client, userdata, flags, rc):
    print("Connected with result code {}".format(rc))

def on_message(client, userdata, message):
    print("Received message: {}".format(message.payload))

client = mqtt.Client(client_id="test_subscriber")
client.on_connect = on_connect
client.on_message = on_message

client.connect(server, 1883, keep_alive)
client.subscribe('test', qos)

client.loop_forever()
