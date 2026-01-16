import json
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from config import CONTROL_GROUP_ID

STATE_FILE = "shared/state.json"

def write_state(data):
    with open(STATE_FILE, "w") as f:
        json.dump(data, f)

def register_handlers(app):

    async def connect(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_chat.id != CONTROL_GROUP_ID:
            return
        if not context.args:
            return await update.message.reply_text("Usage: /connect <group_id>")

        target = int(context.args[0])
        write_state({"action": "connect", "target": target, "volume": 1.0})
        await update.message.reply_text(f"🔗 Connecting to `{target}`")

    async def volume(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_chat.id != CONTROL_GROUP_ID:
            return
        if not context.args:
            return
        vol = int(context.args[0]) / 100
        write_state({"action": "volume", "target": None, "volume": vol})
        await update.message.reply_text(f"🔊 Volume set {int(vol*100)}%")

    async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_chat.id != CONTROL_GROUP_ID:
            return
        write_state({"action": "stop", "target": None, "volume": 1.0})
        await update.message.reply_text("⛔ Relay stopped")

    app.add_handler(CommandHandler("connect", connect))
    app.add_handler(CommandHandler("volume", volume))
    app.add_handler(CommandHandler("stop", stop))
