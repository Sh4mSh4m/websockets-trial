import asyncio
import json

from pprint import pprint

import websockets

# Change channels store
# Channel id is the change_id
CHANNELS = {}

async def notify(change_id):
    """
    For a given channel, send message to 
    every socket registered under that channel
    """
    print(f"NOTIFYING CHANNEL #{change_id}")
    # For garbage collection
    TO_REMOVE = []
    
    # Loop process
    for ws in CHANNELS[change_id]:
        try:
            await ws.send('sync')
        # To be refactored to log 1006 errors
        except:
            # Added to garbage collection
            TO_REMOVE.append(ws)

    # Garbage collection process ==> unregister
    if TO_REMOVE != []:
        for ws in TO_REMOVE:
            await unregister(ws, change_id)
    # Channels control
    pprint(f"{CHANNELS}")

async def register(websocket, message):
    """
    Channels registration. If source is server, 
    Action to notify clients is taken
    """
    change_id = message.get('change_id')

    if message['source'] == 'server':
        if change_id in CHANNELS:
            await notify(message['change_id'])
        else:
            print(f"{change_id} not found")
    elif message['source'] == 'client':
        if change_id in CHANNELS:
            # Append to set of webosockets registered
            CHANNELS[change_id].add(websocket)
        else:
            # Websockets set creation under channel
            CHANNELS.update({change_id: {websocket} })
        # Channels content control
        pprint(f"{CHANNELS}")

async def unregister(websocket, change_id):
    """
    Unregistration of websocket in channel
    """
    if change_id in CHANNELS:
        CHANNELS[change_id].remove(websocket)
    else:
        print(f"{change_id} not found")
    # Channels control
    pprint(f"{CHANNELS}")

async def handler(websocket, path):
    """
    Main handler
    Triage based on action field
    """
    try:
        async for message in websocket:
            message = json.loads(message)
            change_id = message.get('change_id')
            if message['action'] == 'register':
                await register(websocket, message)
            else:
                await unregister(websocket, change_id)
    # To be refactored and log proper exceptions
    except:
        print(f"Error on {websocket}")
        change_id = message.get('change_id')
        await unregister(websocket, change_id)
        pprint(f"{CHANNELS}")

# Server coroutine 
start_server = websockets.serve(handler, "localhost", 8765)


asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
