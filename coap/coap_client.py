import argparse
import asyncio
import json

from aiocoap import *


@asyncio.coroutine
def main(server, data, send_interval):
    protocol = yield from Context.create_client_context()

    while True:
        request = Message(code=PUT, payload=json.dumps(data).encode('utf8'))
        request.set_request_uri('coap://{}/test'.format(server))

        try:
            print("Sending message")
            response = yield from protocol.request(request).response
        except Exception as e:
            print('Failed to fetch resource:')
            print(e)
        else:
            print('Result: ({}) {}'.format(response.code, response.payload))

        yield from asyncio.sleep(send_interval)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create CoAP client')
    parser.add_argument('server')
    parser.add_argument('payload_file', type=argparse.FileType('r'))
    parser.add_argument('send_interval', type=int)

    args = parser.parse_args()

    asyncio.get_event_loop().run_until_complete(main(args.server,
                                                     json.load(args.payload_file),
                                                     args.send_interval))
