import argparse
import json
import os

from persistent_queue import PersistentQueue

import coap_sensor
import coap_gateway
import mqtt_sensor
import mqtt_gateway


def experiment_1_setup(protocol, device_type, data_file):
    """ Run protocols normally """

    if device_type == 'sensor':
        queue_file = '{}.queue'.format(protocol)

        # Delete old queue
        try:
            os.remove(queue_file)
        except FileNotFoundError:
            pass


def experiment_2_setup(protocol, device_type, data_file, queue_size=300):
    """ Run with a built up queue """

    if device_type == 'sensor':
        queue_file = '{}.queue'.format(protocol)

        with open(data_file) as f:
            data = json.load(f)

        # Delete old queue
        try:
            os.remove(queue_file)
        except FileNotFoundError:
            pass

        # Add data points to queue
        queue = PersistentQueue(queue_file)
        for i in range(queue_size):
            queue.push(data)


parser = argparse.ArgumentParser(description='Run experiments')
parser.add_argument('experiment')
parser.add_argument('protocol')
parser.add_argument('device_type')
parser.add_argument('data_file')
parser.add_argument('-i', '--interval', default=60, type=int)
parser.add_argument('--mqtt_broker', default='gatewaymqtt')
parser.add_argument('--coap_sensor', default='sensorcoap')
args = parser.parse_args()


if args.experiment == '1':
    experiment_1_setup(args.protocol, args.device_type, args.data_file)
if args.experiment == '2':
    experiment_2_setup(args.protocol, args.device_type, args.data_file)

if args.protocol == 'coap':
    if args.device_type == 'sensor':
        coap_sensor.main('../data.json', args.interval)
    elif args.device_type == 'gateway':
        coap_gateway.main(args.coap_sensor, args.interval, 8)
    else:
        print("Unknown device type")
elif args.protocol == 'mqtt':
    if args.device_type == 'sensor':
        mqtt_sensor.main(args.mqtt_broker, '../data.json', args.interval)
    elif args.device_type == 'gateway':
        mqtt_gateway.main('localhost')
    else:
        print("Unknown device type")
else:
    print("Unknown protocol")
