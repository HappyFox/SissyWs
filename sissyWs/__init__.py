import asyncio
import json
import logging
import websockets

import sissyWs.display


def set_face(data):
    display = sissyWs.display.get_display()
    display.show_face(data["face"])


handlers = {"face": set_face}


async def dispatcher(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        handlers[data["action"]](data)


def main():
    with sissyWs.display.get_display():
        start_server = websockets.serve(dispatcher, None, 6789)

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
