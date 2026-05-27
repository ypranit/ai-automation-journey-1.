import requests

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am your AI bot.")


async def motivate(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = "https://zenquotes.io/api/random"

    response = requests.get(url)

    data = response.json()

    quote = data[0]["q"]
    author = data[0]["a"]

    await update.message.reply_text(f"{quote}\n\n- {author}")


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_message = update.message.text.lower()

    if "hello" in user_message:
        await update.message.reply_text("Hey there!")

    elif "python" in user_message:
        await update.message.reply_text(
            "Python is amazing for AI and automation."
        )

    elif "motivate" in user_message:

        url = "https://zenquotes.io/api/random"

        response = requests.get(url)

        data = response.json()

        quote = data[0]["q"]
        author = data[0]["a"]

        await update.message.reply_text(f"{quote}\n\n- {author}")

    else:
        await update.message.reply_text(
            "I am still learning 😄"
        )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("motivate", motivate))

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
)

print("Bot is running...")

app.run_polling()