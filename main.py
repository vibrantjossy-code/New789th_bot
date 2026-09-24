import os
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# =========================
# CONFIG
# =========================

TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", "8080"))

if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable is missing")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()


# =========================
# KEYBOARD
# =========================

def main_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📚 Information",
                    callback_data="information"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❓ Help",
                    callback_data="help"
                ),
                InlineKeyboardButton(
                    text="💬 Support",
                    callback_data="support"
                )
            ]
        ]
    )


# =========================
# COMMANDS
# =========================

@dp.message(Command("start"))
async def start_handler(message: types.Message):

    text = (
        "Welcome! 👋\n\n"
        "This bot provides useful information and quick assistance.\n\n"
        "Choose an option below to get started."
    )

    await message.answer(
        text,
        reply_markup=main_keyboard()
    )


@dp.message(Command("help"))
async def help_handler(message: types.Message):

    text = (
        "Available commands:\n\n"
        "/start - Open the main menu\n"
        "/help - View available commands\n"
        "/info - Get information\n"
        "/support - Contact support"
    )

    await message.answer(text)


@dp.message(Command("info"))
async def info_handler(message: types.Message):

    text = (
        "📚 Information\n\n"
        "Use the menu to explore the available features "
        "and information provided by this bot."
    )

    await message.answer(
        text,
        reply_markup=main_keyboard()
    )


@dp.message(Command("support"))
async def support_handler(message: types.Message):

    await message.answer(
        "💬 Support\n\n"
        "If you need assistance, please describe your question "
        "and our support team will respond."
    )


# =========================
# BUTTONS
# =========================

@dp.callback_query(lambda c: c.data == "information")
async def information_callback(callback: types.CallbackQuery):

    await callback.message.edit_text(
        "📚 Information\n\n"
        "Here you can provide your users with useful "
        "information about your service or project.",
        reply_markup=main_keyboard()
    )

    await callback.answer()


@dp.callback_query(lambda c: c.data == "help")
async def help_callback(callback: types.CallbackQuery):

    await callback.message.edit_text(
        "❓ Help\n\n"
        "/start - Main menu\n"
        "/info - Information\n"
        "/support - Support",
        reply_markup=main_keyboard()
    )

    await callback.answer()


@dp.callback_query(lambda c: c.data == "support")
async def support_callback(callback: types.CallbackQuery):

    await callback.message.edit_text(
        "💬 Support\n\n"
        "Send your question here and we'll help you.",
        reply_markup=main_keyboard()
    )

    await callback.answer()


# =========================
# NORMAL TEXT MESSAGES
# =========================

@dp.message()
async def text_handler(message: types.Message):

    await message.answer(
        "Thanks for your message.\n\n"
        "Use /start to open the main menu or /help "
        "to see the available commands."
    )


# =========================
# RAILWAY HEALTH SERVER
# =========================

async def health(request):
    return web.Response(text="Bot is running")


async def start_web_server():
    app = web.Application()
    app.router.add_get("/", health)
    app.router.add_get("/health", health)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(
        runner,
        host="0.0.0.0",
        port=PORT
    )

    await site.start()


# =========================
# MAIN
# =========================

async def main():

    await start_web_server()

    # Remove any old webhook so polling works correctly
    await bot.delete_webhook(drop_pending_updates=True)

    logging.info("Bot started")

    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
