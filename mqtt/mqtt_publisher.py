import argparse
import json
import time

import paho.mqtt.client as mqtt

parser = argparse.ArgumentParser(description='Create MQTT publisher')
parser.add_argument('server')
parser.add_argument('payload_file', type=argparse.FileType('r'))
parser.add_argument('send_interval', type=int)
parser.add_argument('--keep-alive', default=60, type=int)
parser.add_argument('--qos', default=0, type=int)

args = parser.parse_args()

server = args.server
data = json.load(args.payload_file)
send_interval = args.send_interval
keep_alive = args.keep_alive
qos = args.qos

def on_connect(client, userdata, flags, rc):
    print("Connected with result code {}".format(rc))

def on_disconnect(client, userdata, rc):
    print("Disconnected from broker")

def on_publish(client, userdata, mid):
    print("Published {}".format(mid))

client = mqtt.Client(client_id="test_publisher")
client.on_connect = on_connect
client.on_publish = on_publish
client.on_disconnect = on_disconnect

client.connect(server, 1883, keep_alive)

client.loop_start()

while True:
    result = client.publish('test', payload=json.dumps(data), qos=qos)
    print("Published with result: {}".format(result))

    time.sleep(send_interval)

client.loop_stop()
