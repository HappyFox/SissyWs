import asyncio
import json
import logging
import websockets

logging.basicConfig()


def set_face(data):
    print(data["face"])


handlers = {"face": set_face}

async def dispatcher(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        handlers[data["action"]](data)

start_server = websockets.serve(dispatcher, None, 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
