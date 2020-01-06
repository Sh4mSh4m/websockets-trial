import asyncio
import json
import websockets

async def send_msg():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        message = {
            "action": "register",
            "source": "server",
            "change_id": "1",
        }
        await websocket.send(json.dumps(message))
        print(f"Message sent wesh")

asyncio.get_event_loop().run_until_complete(send_msg())
