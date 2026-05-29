import os
from dotenv import load_dotenv

load_dotenv()

import json
import asyncio
import requests
import python_weather

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
# TOKENS
# =========================

TOKEN = os.getenv("TOKEN")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  


NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# =========================
# OPENROUTER CLIENT
# =========================

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

# =========================
# USER MODES
# =========================

user_modes = {}

# =========================
# MEMORY
# =========================

def load_memory(user_id):

    file = f"{user_id}.json"

    if os.path.exists(file):

        with open(file, "r") as f:
            return json.load(f)

    return [
        {
            "role": "system",
            "content": (
                "You are a helpful AI mentor."
            )
        }
    ]


def save_memory(user_id, messages):

    file = f"{user_id}.json"

    with open(file, "w") as f:
        json.dump(messages, f)

# =========================
# NOTES
# =========================

def load_notes():

    if os.path.exists("notes.json"):

        with open("notes.json", "r") as f:
            return json.load(f)

    return {}


def save_notes(notes):

    with open("notes.json", "w") as f:
        json.dump(notes, f)

# =========================
# COMMANDS
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🔥 AI Bot is alive!"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "/start /help /note /notes /weather /search"
    )

# =========================
# WEATHER
# =========================

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) == 0:

        await update.message.reply_text(
            "Usage: /weather city"
        )

        return

    city = " ".join(context.args)

    async with python_weather.Client() as weather_client:

        weather = await weather_client.get(city)

        message = (
            f"🌤 Weather in {city}\n\n"
            f"Temperature: {weather.temperature}°C\n"
            f"Condition: {weather.description}"
        )

        await update.message.reply_text(message)

# =========================
# NOTES
# =========================

async def note(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = str(update.message.from_user.id)

    notes = load_notes()

    if len(context.args) == 0:

        await update.message.reply_text(
            "Usage: /note text"
        )

        return

    text = " ".join(context.args)

    if user_id not in notes:
        notes[user_id] = []

    notes[user_id].append(text)

    save_notes(notes)

    await update.message.reply_text(
        "📝 Note saved!"
    )


async def notes(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = str(update.message.from_user.id)

    notes_data = load_notes()

    user_notes = notes_data.get(user_id, [])

    if len(user_notes) == 0:

        await update.message.reply_text(
            "No notes saved."
        )

        return

    message = "📝 Your Notes\n\n"

    for index, note in enumerate(user_notes, start=1):

        message += f"{index}. {note}\n"

    await update.message.reply_text(message)

# =========================
# SEARCH
# =========================

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) == 0:

        await update.message.reply_text(
            "Usage: /search topic"
        )

        return

    query = " ".join(context.args)

    await update.message.reply_text(
        f"🔎 Searching: {query}"
    )

    try:

        url = (
            f"https://newsapi.org/v2/everything?"

        f"q={query}&apiKey={NEWS_API_KEY}"

        )

        data = requests.get(url).json()

        articles = data.get("articles", [])

        if len(articles) == 0:

            await update.message.reply_text(
                "No results found."
            )

            return

        search_text = ""

        for article in articles[:5]:

            title = article.get("title", "")
            description = article.get("description", "")

            search_text += (
                f"{title}\n{description}\n\n"
            )

        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Summarize news simply."
                    )
                },
                {
                    "role": "user",
                    "content": search_text
                }
            ]
        )

        reply = response.choices[0].message.content

        await update.message.reply_text(reply)

    except Exception as e:

        await update.message.reply_text(
            f"Search error: {e}"
        )

# =========================
# AI CHAT
# =========================

async def generate_ai_reply(user_id, user_text):

    messages = load_memory(user_id)

    messages.append(
        {
            "role": "user",
            "content": user_text
        }
    )

    response = await asyncio.to_thread(
        lambda: client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=messages
        )
    )

    reply = response.choices[0].message.content

    messages.append(
        {
            "role": "assistant",
            "content": reply
        }
    )

    save_memory(user_id, messages)

    return reply

# =========================
# VOICE AI
# =========================

async def voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.voice:
        return

    user_id = update.message.from_user.id

    await update.message.reply_text(
        "🎤 Listening..."
    )

    try:

        file = await context.bot.get_file(
            update.message.voice.file_id
        )

        temp_path = (
            f"voice_{user_id}.ogg"
        )

        await file.download_to_drive(
            custom_path=temp_path
        )

        def transcribe():

    import whisper

    model = whisper.load_model("base")

    result = model.transcribe(
        temp_path
    )

    return result["text"]


        transcript = await asyncio.to_thread(
            transcribe
        )

        await update.message.reply_text(
            f"📝 Transcript:\n{transcript}"
        )

        reply = await generate_ai_reply(
            user_id,
            transcript
        )

        await update.message.reply_text(reply)

        if os.path.exists(temp_path):
            os.remove(temp_path)

    except Exception as e:

        await update.message.reply_text(
            f"Voice error: {e}"
        )

# =========================
# NORMAL CHAT
# =========================

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id

    user_text = update.message.text

    reply = await generate_ai_reply(
        user_id,
        user_text
    )

    await update.message.reply_text(reply)

# =========================
# APP START
# =========================

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("weather", weather))
app.add_handler(CommandHandler("note", note))
app.add_handler(CommandHandler("notes", notes))
app.add_handler(CommandHandler("search", search))

app.add_handler(
    MessageHandler(filters.VOICE, voice_message)
)

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        chat
    )
)

print("Bot running...")

app.run_polling()
