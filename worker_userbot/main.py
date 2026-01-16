import asyncio, json
from pyrogram import Client
from config import API_ID, API_HASH, SESSION_NAME
from worker_userbot.vc_bridge import VCBridge

STATE_FILE = "shared/state.json"

app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)
bridge = VCBridge(app)

async def watcher():
    last = None
    while True:
        try:
            with open(STATE_FILE) as f:
                state = json.load(f)
        except:
            await asyncio.sleep(1)
            continue

        if state != last:
            action = state.get("action")

            if action == "connect":
                await bridge.start(state["target"])

            elif action == "volume":
                bridge.set_volume(state["volume"])

            elif action == "stop":
                await bridge.stop()

            last = state

        await asyncio.sleep(1)

@app.on_ready()
async def ready():
    print("👤 Userbot Ready")
    asyncio.create_task(watcher())

app.run()
