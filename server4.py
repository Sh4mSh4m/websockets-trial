import asyncio
import websockets
import json
from pprint import pprint

CHANNELS = {}

async def notify(change_id):
    print(f"yeahh notifying for {change_id}")
    #await asyncio.wait([ws.send('sync') for ws in CHANNELS[change_id]])
    for ws in CHANNELS[change_id]:
        try:
            print(f"sending to {ws}")
            await ws.send('sync')
        except:
            print("caught existing failed ws")
            print(f"{dir(ws)}")
    pprint(f"{CHANNELS}")

async def register(websocket, message):
    change_id = message.get('change_id')
    print(f"CHANGEID is: {change_id}")
    if message['source'] == 'server':
        if change_id in CHANNELS:
            print(f"send message to websockets linked to change")
            await notify(message['change_id'])
        else:
            print(f"{change_id} not found")
    elif message['source'] == 'client':
        if change_id in CHANNELS:
            CHANNELS[change_id].append(websocket)
        else:
            CHANNELS.update({change_id: [websocket]})
        pprint(f"{CHANNELS}")

async def unregister(websocket, change_id):
    CHANNELS[change_id].remove(websocket)
    pprint(f"{CHANNELS}")

async def handler(websocket, path):
    try:
        async for message in websocket:
            message = json.loads(message)
            change_id = message.get('change_id')
            if message['action'] == 'register':
                await register(websocket, message)
            else:
                await unregister(websocket, change_id)
    except:
        print('CAUGHT IT')
        change_id = message.get('change_id')
        await unregister(websocket, change_id)
        pprint(f"{CHANNELS}")


start_server = websockets.serve(handler, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
