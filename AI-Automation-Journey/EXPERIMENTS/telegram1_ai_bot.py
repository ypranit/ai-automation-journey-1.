import os
import json
import requests

from openai import OpenAI
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# =========================
# ENV VARIABLES (IMPORTANT)
# =========================

TOKEN = os.getenv("TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# =========================
# AI CLIENT
# =========================

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

# =========================
# MEMORY SYSTEM
# =========================

def load_memory(user_id):
    file = f"{user_id}.json"

    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)

    return [
        {
            "role": "system",
            "content": "You are a helpful AI mentor for Python, AI, and automation."
        }
    ]


def save_memory(user_id, messages):
    file = f"{user_id}.json"
    with open(file, "w") as f:
        json.dump(messages, f)

# =========================
# COMMANDS
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 AI Bot is alive!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start /help /motivate /clear")


async def motivate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://zenquotes.io/api/random"
    data = requests.get(url).json()

    quote = data[0]["q"]
    author = data[0]["a"]

    await update.message.reply_text(f"{quote}\n- {author}")


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    default = [
        {
            "role": "system",
            "content": "You are a helpful AI mentor for Python, AI, and automation."
        }
    ]

    save_memory(user_id, default)
    await update.message.reply_text("Memory cleared 🔄")

# =========================
# CHAT FUNCTION
# =========================

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_text = update.message.text

    messages = load_memory(user_id)
    messages.append({"role": "user", "content": user_text})

    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=messages
    )

    reply = response.choices[0].message.content

    messages.append({"role": "assistant", "content": reply})
    save_memory(user_id, messages)

    await update.message.reply_text(reply)

# =========================
# APP START
# =========================

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("motivate", motivate))
app.add_handler(CommandHandler("clear", clear))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

print("Bot running...")
app.run_polling()