import json
import os
import requests

from openai import OpenAI

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    filters,
    ContextTypes,
)

# -------------------------
# TELEGRAM TOKEN
# -------------------------

TOKEN = os.getenv("TOKEN")

# -------------------------
# OPENROUTER AI
# -------------------------

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")

)

# -------------------------
# MEMORY FUNCTION
# -------------------------

def load_memory(user_id):

    filename = f"{user_id}.json"

    if os.path.exists(filename):

        with open(filename, "r") as file:
            messages = json.load(file)

    else:

        messages = [

            {
                "role": "system",
                "content": (
                    "You are a smart AI mentor helping a beginner "
                    "learn Python, AI automation, APIs, "
                    "and software development."
                )
            }

        ]

    return messages

# -------------------------
# SAVE MEMORY
# -------------------------

def save_memory(user_id, messages):

    filename = f"{user_id}.json"

    with open(filename, "w") as file:
        json.dump(messages, file)

# -------------------------
# START COMMAND
# -------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Hello! I am your AI Assistant Bot 😄"
    )

# -------------------------
# HELP COMMAND
# -------------------------

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    help_text = """
Available Commands:

/start - Start the bot
/help - Show commands
/motivate - Get motivation
/clear - Clear memory
"""

    await update.message.reply_text(help_text)

# -------------------------
# MOTIVATION COMMAND
# -------------------------

async def motivate(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = "https://zenquotes.io/api/random"

    response = requests.get(url)

    data = response.json()

    quote = data[0]["q"]
    author = data[0]["a"]

    await update.message.reply_text(
        f"{quote}\n\n- {author}"
    )

# -------------------------
# CLEAR MEMORY
# -------------------------

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id

    messages = [

        {
            "role": "system",
            "content": (
                "You are a smart AI mentor helping a beginner "
                "learn Python, AI automation, APIs, "
                "and software development."
            )
        }

    ]

    save_memory(user_id, messages)

    await update.message.reply_text(
        "Your memory was cleared."
    )

# -------------------------
# AI CHAT
# -------------------------

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id

    user_message = update.message.text

    messages = load_memory(user_id)

    messages.append(
        {"role": "user", "content": user_message}
    )

    completion = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=messages
    )

    reply = completion.choices[0].message.content

    messages.append(
        {"role": "assistant", "content": reply}
    )

    save_memory(user_id, messages)

    await update.message.reply_text(reply)

# -------------------------
# START BOT
# -------------------------

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("motivate", motivate))
app.add_handler(CommandHandler("clear", clear))

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
)

print("AI Telegram Bot Running...")

app.run_polling()