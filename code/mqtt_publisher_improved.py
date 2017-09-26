import argparse
import json
import time
from collections import deque

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

messages = deque()
sending = False


def on_publish(client, userdata, mid):
    global sending
    print("Finished publishing: {}".format(mid))

    if len(messages) == 0:
        sending = False
    else:
        publish_message(client)


def on_connect(client, userdata, flags, rc):
    print("Connected with result: {}".format(rc))


def publish_message(client):
    global sending
    message = messages[0]

    rc, mid = client.publish(**message)
    print("Published message: {}".format(rc))

    if rc != mqtt.MQTT_ERR_NO_CONN:
        # The message was sent successfully
        messages.popleft()
    else:
        sending = False


client = mqtt.Client(client_id='test_publisher')
client.on_publish = on_publish
client.on_connect = on_connect
client.connect(server, 1883, keep_alive)

client.loop_start()
while True:
    messages.append({'topic': 'test', 'payload': json.dumps(data), 'qos': qos})
    print("Added a new message to the queue ({})".format(len(messages)))

    if not sending:
        sending = True
        publish_message(client)

    time.sleep(send_interval)

client.loop_stop()

