import asyncio
import os
import urllib.parse
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

ROOT = os.path.dirname(os.path.dirname(__file__))
load_dotenv(os.path.join(ROOT, ".env"))
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")
router = Router()

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎬 Movies"), KeyboardButton(text="📺 TV Shows")],
        [KeyboardButton(text="🎞️ Shorts"), KeyboardButton(text="📡 Live TV")],
        [KeyboardButton(text="🔎 Search"), KeyboardButton(text="💎 Premium")],
        [KeyboardButton(text="🌐 Language"), KeyboardButton(text="👤 Help")],
    ],
    resize_keyboard=True,
)

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "🙏 <b>Welcome to Shree Krishna</b>\\n\\n"
        "Movies, TV Shows, Shorts and Live TV — browse authorized content here.\\n"
        "Use the buttons below or /search title.",
        reply_markup=keyboard,
    )

@router.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer(
        "<b>Shree Krishna Bot Help</b>\\n"
        "/start — Main menu\\n"
        "/search title — Search content\\n"
        "/shows — Browse TV shows\\n"
        "/premium — Premium information"
    )

@router.message(Command("premium"))
async def premium(message: Message):
    await message.answer(
        "💎 <b>Premium</b>\\n"
        "Premium plans will be configured by the admin. "
        "Do not send payment to anyone until official payment verification is enabled."
    )

@router.message(Command("shows"))
async def shows(message: Message):
    await show_content(message, "show")

@router.message(Command("search"))
async def search(message: Message):
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Use: /search movie or show name")
        return
    await show_content(message, query=parts[1])

@router.message()
async def menu(message: Message):
    text = (message.text or "").strip()
    mapping = {
        "🎬 Movies": ("movie", None),
        "📺 TV Shows": ("show", None),
        "🎞️ Shorts": ("short", None),
        "📡 Live TV": ("live", None),
    }
    if text in mapping:
        kind, query = mapping[text]
        await show_content(message, kind=kind, query=query)
    elif text == "🌐 Language":
        await message.answer("Supported categories: Hindi, English, Bangla, Gujarati, Rajasthani, Urdu, Tamil, Telugu. Language filters will be added to the connected app/API.")
    elif text == "💎 Premium":
        await premium(message)
    elif text == "👤 Help":
        await help_cmd(message)
    elif text == "🔎 Search":
        await message.answer("Search with /search title")
    else:
        await message.answer("Use /search title or choose a menu button.")

async def show_content(message: Message, kind: str | None = None, query: str | None = None):
    try:
        import urllib.request, json
        params = {}
        if kind: params["kind"] = kind
        url = BACKEND_URL + "/api/content"
        if params:
            url += "?" + urllib.parse.urlencode(params)
        with urllib.request.urlopen(url, timeout=5) as response:
            items = json.loads(response.read().decode("utf-8"))
        if query:
            items = [x for x in items if query.lower() in x["title"].lower()]
        if not items:
            await message.answer("No published content found yet. Admin can add authorized content through the API.")
            return
        lines = []
        for item in items[:15]:
            mark = "💎 " if item.get("is_premium") else ""
            lines.append(f"{mark}<b>{item['title']}</b> · {item['language']} · {item['category']}")
            if item.get("poster_url"): lines.append(item["poster_url"])
            if item.get("stream_url"): lines.append("Stream available in the connected app/player.")
            lines.append("")
        await message.answer("\\n".join(lines), disable_web_page_preview=False)
    except Exception:
        await message.answer("Content service is not reachable. Please start the backend and check BACKEND_URL.")

async def main():
    if not TOKEN or TOKEN == "put_your_bot_token_here":
        raise RuntimeError("Set TELEGRAM_BOT_TOKEN in the root .env file first.")
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
