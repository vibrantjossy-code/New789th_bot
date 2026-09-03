import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Logging setup for monitoring container health on Railway
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Retrieve Telegram Bot Token from Environment Variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Triggered on /start or when users enter from Telegram Ads."""
    keyboard = [
        [InlineKeyboardButton("ℹ️ เกี่ยวกับเรา", callback_data="about")],
        [InlineKeyboardButton("❓ คำถามที่พบบ่อย (FAQ)", callback_data="faq")],
        [InlineKeyboardButton("📩 ติดต่อฝ่ายบริการลูกค้า", callback_data="contact")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "ยินดีต้อนรับ! 👋\n\n"
        "เราให้บริการโซลูชันและการสนับสนุนเพื่อช่วยจัดการกระบวนการทำงานของคุณ\n"
        "โปรดเลือกเมนูด้านล่างเพื่อดูรายละเอียดเพิ่มเติม"
    )
    
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.edit_message_text(welcome_text, reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mandatory /help response required by Telegram Ads Policy."""
    help_text = (
        "คำสั่งที่ใช้งานได้:\n"
        "/start - เปิดเมนูหลัก\n"
        "/about - ข้อมูลเกี่ยวกับเรา\n"
        "/help - แสดงเมนูช่วยเหลือนี้\n\n"
        "คุณสามารถใช้ปุ่มด้านล่างในข้อความเพื่อเลือกรายการที่ต้องการได้ทันที"
    )
    await update.message.reply_text(help_text)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mandatory /about response detailing service identity."""
    about_text = (
        "เกี่ยวกับแพลตฟอร์มของเรา:\n\n"
        "เราให้บริการเครื่องมือและการสนับสนุนทางเทคนิคเพื่อเพิ่มประสิทธิภาพการทำงาน "
        "เป้าหมายของเราคือการให้บริการที่แม่นยำ โปร่งใส และตอบโจทย์ความต้องการของคุณ"
    )
    await update.message.reply_text(about_text)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles inline menu navigation."""
    query = update.callback_query
    await query.answer()

    keyboard = [[InlineKeyboardButton("« กลับสู่เมนูหลัก", callback_data="main_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if query.data == "about":
        text = (
            "📌 เกี่ยวกับเรา:\n\n"
            "เราพัฒนาเครื่องมือดิจิทัลสำหรับการจัดการ คุณสามารถเรียกดูคำถามที่พบบ่อย "
            "หรือติดต่อทีมงานฝ่ายบริการลูกค้าของเราได้โดยตรงผ่านบอทนี้"
        )
        await query.edit_message_text(text=text, reply_markup=reply_markup)

    elif query.data == "faq":
        faq_keyboard = [
            [InlineKeyboardButton("ติดต่อฝ่ายบริการได้อย่างไร?", callback_data="faq_contact")],
            [InlineKeyboardButton("เวลาทำการคือช่วงไหน?", callback_data="faq_hours")],
            [InlineKeyboardButton("« กลับสู่เมนูหลัก", callback_data="main_menu")],
        ]
        await query.edit_message_text(
            "คำถามที่พบบ่อย (FAQ):\nโปรดเลือกหัวข้อที่ต้องการทราบ:",
            reply_markup=InlineKeyboardMarkup(faq_keyboard)
        )

    elif query.data == "faq_contact":
        text = "คุณสามารถติดต่อทีมงานได้โดยตรงผ่านปุ่ม 'ติดต่อฝ่ายบริการลูกค้า' ที่หน้าเมนูหลัก"
        await query.edit_message_text(text=text, reply_markup=reply_markup)

    elif query.data == "faq_hours":
        text = "ฝ่ายบริการลูกค้าของเราเปิดทำการวันจันทร์ - วันศุกร์ เวลา 09:00 - 18:00 น. (UTC)"
        await query.edit_message_text(text=text, reply_markup=reply_markup)

    elif query.data == "contact":
        text = (
            "📩 ติดต่อฝ่ายบริการลูกค้า:\n\n"
            "หากคุณมีข้อสงสัย โปรดทิ้งข้อความไว้ "
            "ทีมงานของเราจะติดต่อกลับภายใน 24 ชั่วโมง"
        )
        await query.edit_message_text(text=text, reply_markup=reply_markup)

    elif query.data == "main_menu":
        await start(update, context)

def main() -> None:
    if not TOKEN:
        raise ValueError("Error: TELEGRAM_BOT_TOKEN environment variable not set.")

    application = Application.builder().token(TOKEN).build()

    # Core commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))

    # Inline menu callbacks
    application.add_handler(CallbackQueryHandler(button_handler))

    # Run polling loop
    logger.info("Bot started successfully...")
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
