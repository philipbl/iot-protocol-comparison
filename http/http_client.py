import argparse
import json
import time

import requests

parser = argparse.ArgumentParser(description='Create HTTP client')
parser.add_argument('server')
parser.add_argument('payload_file', type=argparse.FileType('r'))
parser.add_argument('send_interval', type=int)

args = parser.parse_args()

server = args.server
data = json.load(args.payload_file)
send_interval = args.send_interval

while True:
    print("Sending message")
    requests.post("http://{}:5000/test".format(server), json=data)
    time.sleep(send_interval)
