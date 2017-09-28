import argparse
import json
from threading import Thread
import time

import paho.mqtt.client as mqtt
from persistent_queue import PersistentQueue


def start_sensors(queue, data_file, interval):
    with open(data_file) as f:
        data = json.load(f)

    while True:
        queue.push(data)
        print("Generating new data... ({})".format(len(queue)))

        time.sleep(interval)


def main(broker, data_file, interval):
    print("Loading queue...")
    queue = PersistentQueue('mqtt.queue')

    print("Starting producer")
    producer = Thread(target=start_sensors,
                      args=(queue, data_file, interval))
    producer.start()

    print("Starting MQTT publisher...")
    client = mqtt.Client()
    client.connect(broker)
    client.loop_start()

    while True:
        data = queue.peek(blocking=True)

        # Convert all byte strings to strings
        print("Publishing data")

        info = client.publish('devices/sensor001/data',
                              payload=json.dumps(data),
                              qos=1)
        info.wait_for_publish()
        queue.delete()
        queue.flush()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create MQTT publisher')
    parser.add_argument('broker')
    parser.add_argument('data_file')
    parser.add_argument('-i', '--interval', type=int, default=2)
    args = parser.parse_args()

    main(args.broker, args.data_file, args.interval)
