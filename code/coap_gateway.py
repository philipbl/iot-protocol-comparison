import argparse
import asyncio
import json
import struct

from aiocoap import *


async def start(server, update_time, requesting):
    protocol = await Context.create_client_context()
    total = 0
    acking = 0

    while True:
        payload = struct.pack('!HH', acking, requesting)
        request = Message(code=GET, payload=payload)
        request.set_request_uri('coap://{}/data'.format(server))

        try:
            print("Sending request for data...")
            print(request)
            response = await protocol.request(request).response
        except Exception as e:
            print('Failed to fetch resource')
            print(e)
            print("Waiting...")
            acking = 0
            await asyncio.sleep(update_time)
            continue

        try:
            data = json.loads(response.payload.decode())
            acking = len(data)
            total += acking
            print("Received: {} ({})".format(acking, total))
        except Exception as e:
            print(e)
            print("Waiting...")
            acking = 0
            await asyncio.sleep(update_time)
            continue

        if acking == requesting:
            print("Requesting more data...")
        else:
            print("Done requesting data...")
            await asyncio.sleep(update_time)


def main(server, update_time, requesting):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start(server, update_time, requesting))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create CoAP client')
    parser.add_argument('server')
    parser.add_argument('-u', '--update_time', type=int, default=10)
    parser.add_argument('-r', '--requesting', type=int, default=10)
    args = parser.parse_args()

    main(args.server, args.update_time, args.requesting)
