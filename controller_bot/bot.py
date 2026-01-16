from telegram.ext import ApplicationBuilder
from config import BOT_TOKEN
from controller_bot.handlers import register_handlers

app = ApplicationBuilder().token(BOT_TOKEN).build()
register_handlers(app)

print("🤖 Controller Bot Started")
app.run_polling()
