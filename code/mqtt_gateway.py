import argparse
import json
import time

import paho.mqtt.client as mqtt

total = 0

def on_connect(client, userdata, flags, rc):
    print("Connected with result code {}".format(rc))
    client.subscribe('devices/+/data', 1)


def on_message(client, userdata, message):
    global total
    total += 1
    print("Received message ({})".format(total))


def main(broker):
   client = mqtt.Client()
   client.on_connect = on_connect
   client.on_message = on_message
   client.connect(broker)

   client.loop_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create MQTT subscriber')
    parser.add_argument('broker')
    args = parser.parse_args()

    main(args.broker)


