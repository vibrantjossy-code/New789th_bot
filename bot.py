import logging
import os
from pathlib import Path
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Base directory relative to this script
BASE_DIR = Path(__file__).resolve().parent
IMAGE_PATH = BASE_DIR / "banner.jpg"

# Text Messages
WELCOME_TEXT = (
    "สวัสดี {user_name} ยินดีต้อนรับสู่ เว็บ UFANEXT ตรงจาก UFABET! 🎉\n\n"
    "🧧💥 สมัครวันนี้รับเครดิตฟรี 300 บาท หรือฟรีสปิน 300 ครั้ง 💥🧧\n"
    "🎰 คืนเงินเดิมพันทุกวัน!\n"
    "❤️ แจ็คพอตแตกทุกชั่วโมง! 😮 คุณอาจเป็นคนต่อไป 🔥\n\n"
    "🎁 ลุ้นโชคกับรางวัล LUCKY SPIN REWARDS !!\n"
    "💥รับรางวัลเงินสด! 20,545,200 บาท ที่นี่!!💥\n"
    "เราให้โบนัสต้อนรับ 1,500 บาท แก่คุณหากเข้าร่วมวันนี้!!\n\n"
    "🎲 สมัครคลิ๊ก https://ufanext.cc/register/\n"
    "📲 เว็บ UFANEXT https://ufanext.cc"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command by sending the local image with formatted text and buttons."""
    user = update.effective_user
    user_name = user.first_name if user.first_name else user.full_name

    # Create inline link buttons
    keyboard = [
        [
            InlineKeyboardButton("🎲 สมัครสมาชิก (Register)", url="https://ufanext.cc/register/"),
        ],
        [
            InlineKeyboardButton("📲 เข้าสู่เว็บไซต์ (Website)", url="https://ufanext.cc"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Insert user's name dynamically into the Thai promo text
    formatted_message = WELCOME_TEXT.format(user_name=user_name)

    if IMAGE_PATH.is_file():
        with open(IMAGE_PATH, "rb") as photo_file:
            await update.message.reply_photo(
                photo=photo_file,
                caption=formatted_message,
                reply_markup=reply_markup
            )
    else:
        # Fallback to plain text if image file is missing
        logger.warning(f"Image not found at path: {IMAGE_PATH}. Sending text only.")
        await update.message.reply_text(
            text=formatted_message,
            reply_markup=reply_markup
        )

def main() -> None:
    """Start the bot."""
    token = os.getenv("BOT_TOKEN")

    if not token:
        logger.error("No BOT_TOKEN found in environment variables!")
        return

    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler("start", start))

    logger.info("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
