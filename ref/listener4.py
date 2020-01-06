import asyncio
import json
import websockets

async def listen_msg():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        message = {
            "action": "register",
            "source": "client",
            "change_id": "2",
        }
        await websocket.send(json.dumps(message))
        print(f"listener registered wesh")
        signal = await websocket.recv()
        print(signal)
        message = {
            "action": "unregister",
            "change_id": "2",
        }
        await websocket.send(json.dumps(message))
        print('signed off properly')

asyncio.get_event_loop().run_until_complete(listen_msg())
