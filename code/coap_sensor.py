import argparse
import asyncio
import datetime
import json
import logging
import struct

import aiocoap.resource as resource
import aiocoap
from persistent_queue import PersistentQueue


async def start_sensors(queue, data_file, interval):
    with open(data_file) as f:
        data = json.load(f)

    while True:
        queue.push(data)
        print("Generating new data... ({})".format(len(queue)))

        await asyncio.sleep(interval)


class DataResource(aiocoap.resource.Resource):
    def __init__(self, queue):
        super(DataResource, self).__init__()
        self.queue = queue

    async def render_get(self, request):
        print(request)
        acking, requesting, = struct.unpack('!HH', request.payload)
        print("Received request: ACK {} REQUEST {}".format(acking, requesting))

        self.queue.delete(acking)
        self.queue.flush()

        data = self.queue.peek(requesting)
        payload = json.dumps(data).encode()
        response = aiocoap.Message(code=aiocoap.CONTENT, payload=payload)
        return response


def main():
    parser = argparse.ArgumentParser(description='Create CoAP client')
    parser.add_argument('data_file')
    parser.add_argument('-i', '--interval', type=int, default=2)
    args = parser.parse_args()

    print("Loading queue...")
    queue = PersistentQueue('coap.queue')

    print("Starting producer")
    producer = start_sensors(queue, args.data_file, args.interval)

    print("Starting server...")
    root = resource.Site()
    root.add_resource(("data",), DataResource(queue))

    server = aiocoap.Context.create_server_context(root)

    test = asyncio.wait([producer, server])
    asyncio.get_event_loop().run_until_complete(test)


if __name__ == "__main__":
    main()
