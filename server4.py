import asyncio
import websockets
import json
from pprint import pprint

CHANNELS = {}

async def notify(change_id):
    print(f"SEND LOOP FOR CHANGE#{change_id}")
    #await asyncio.wait([ws.send('sync') for ws in CHANNELS[change_id]])
    TO_REMOVE = []
    for ws in CHANNELS[change_id]:
        try:
            await ws.send('sync')
            print(f"SENT to {ws}")
        except:
            print(f"caught existing failed {ws}")
            #print(f"{dir(ws)}")
            TO_REMOVE.append(ws)
    if TO_REMOVE != []:
        for ws in TO_REMOVE:
            await unregister(ws, change_id)
    pprint(f"{CHANNELS}")

async def register(websocket, message):
    change_id = message.get('change_id')
    print(f"CHANGEID is: {change_id}")
    if message['source'] == 'server':
        if change_id in CHANNELS:
            await notify(message['change_id'])
        else:
            print(f"{change_id} not found")
    elif message['source'] == 'client':
        if change_id in CHANNELS:
            CHANNELS[change_id].add(websocket)
        else:
            CHANNELS.update({change_id: {websocket} })
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
