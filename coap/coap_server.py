import argparse
import asyncio
import datetime
import logging

import aiocoap.resource as resource
import aiocoap


class TestResource(resource.Resource):
    def __init__(self):
        super(TestResource, self).__init__()

    @asyncio.coroutine
    def render_get(self, request):
        payload = b"this is a test."
        response = aiocoap.Message(code=aiocoap.CONTENT, payload=payload)
        return response

    @asyncio.coroutine
    def render_put(self, request):
        print('PUT payload: %s' % request.payload)
        self.content = request.payload
        payload = b""
        return aiocoap.Message(code=aiocoap.CHANGED, payload=payload)


def main():
    print("Starting server...")
    root = resource.Site()
    root.add_resource(("test",), TestResource())

    asyncio.async(aiocoap.Context.create_server_context(root))
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
