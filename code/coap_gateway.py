import argparse
import asyncio
import json
import struct

from aiocoap import *


async def main(server, update_time, request_interval, requesting):
    protocol = await Context.create_client_context()
    acking = 0

    while True:
        payload = struct.pack('!HH', acking, requesting)
        request = Message(code=GET, payload=payload)
        request.set_request_uri('coap://{}/data'.format(server))

        try:
            print("Sending request for data...")
            response = await protocol.request(request).response
        except Exception as e:
            print('Failed to fetch resource:')
            print(e)
            acking = 0
            await asyncio.sleep(update_time)
            continue

        try:
            data = json.loads(response.payload.decode())
            acking = len(data)
            print("Received: {}".format(acking))
        except Exception as e:
            print(e)
            acking = 0
            await asyncio.sleep(update_time)
            continue

        if acking == requesting:
            print("Requesting more data...")
            await asyncio.sleep(request_interval)
        else:
            print("Done requesting data...")
            await asyncio.sleep(update_time)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create CoAP client')
    parser.add_argument('server')
    parser.add_argument('-i', '--request_interval', type=int, default=1)
    parser.add_argument('-u', '--update_time', type=int, default=10)
    parser.add_argument('-r', '--requesting', type=int, default=10)

    args = parser.parse_args()

    asyncio.get_event_loop().run_until_complete(main(args.server,
                                                     args.update_time,
                                                     args.request_interval,
                                                     args.requesting))
