import argparse
import json
from threading import Thread
import time

import paho.mqtt.client as mqtt
from persistent_queue import PersistentQueue


def start_sensors(queue, interval):
    while True:
        data = {'small': 500, 'large': 123}
        queue.push(data)
        print("Generating new data... ({})".format(len(queue)))

        time.sleep(interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create MQTT publisher')
    parser.add_argument('broker')
    parser.add_argument('-i', '--interval', type=int, default=2)
    args = parser.parse_args()

    print("Loading queue...")
    queue = PersistentQueue('mqtt.queue')

    print("Starting producer")
    producer = Thread(target=start_sensors,
                      args=(queue, args.interval))
    producer.start()

    print("Starting MQTT publisher...")
    client = mqtt.Client()
    client.connect(args.broker)
    client.loop_start()

    while True:
        data = queue.peek(blocking=True)

        # Convert all byte strings to strings
        print("Publishing: {}".format(data))

        info = client.publish('devices/sensor001/data',
                              payload=json.dumps(data),
                              qos=1)
        info.wait_for_publish()
        queue.delete()
        queue.flush()
