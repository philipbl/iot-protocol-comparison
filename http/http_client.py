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

s = requests.Session()

while True:
    print("Sending message")
    r = s.post("http://{}:5000/test".format(server), json=data)
    print("Response: {}".format(r.text))

    time.sleep(send_interval)
