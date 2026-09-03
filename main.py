import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Logging setup for monitoring container health on Render
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Retrieve Telegram Bot Token from Environment Variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Triggered on /start or when users enter from Telegram Ads."""
    keyboard = [
        [InlineKeyboardButton("ℹ️ About Us", callback_data="about")],
        [InlineKeyboardButton("❓ Frequently Asked Questions", callback_data="faq")],
        [InlineKeyboardButton("📩 Contact Support", callback_data="contact")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "Welcome! 👋\n\n"
        "We offer specialized services to streamline your operations and workflow.\n"
        "Please choose an option below to learn more about our services."
    )
    
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.edit_message_text(welcome_text, reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mandatory /help response required by Telegram Ads Policy."""
    help_text = (
        "Available commands:\n"
        "/start - Launch the main menu\n"
        "/about - Learn more about our company\n"
        "/help - Display this support menu\n\n"
        "You can also use the inline buttons in the chat to navigate."
    )
    await update.message.reply_text(help_text)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mandatory /about response detailing service identity."""
    about_text = (
        "About Our Platform:\n\n"
        "We assist businesses and individuals with automated workflow solutions, "
        "consulting, and technical support. Our goal is to provide reliable, "
        "transparent services tailored to your needs."
    )
    await update.message.reply_text(about_text)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles inline menu navigation to ensure clean interaction."""
    query = update.callback_query
    await query.answer()

    keyboard = [[InlineKeyboardButton("« Back to Main Menu", callback_data="main_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if query.data == "about":
        text = (
            "📌 About Us:\n\n"
            "We build practical digital management tools. Use this bot to browse FAQs "
            "or connect directly with our support staff."
        )
        await query.edit_message_text(text=text, reply_markup=reply_markup)

    elif query.data == "faq":
        faq_keyboard = [
            [InlineKeyboardButton("How do I contact support?", callback_data="faq_contact")],
            [InlineKeyboardButton("What are your operating hours?", callback_data="faq_hours")],
            [InlineKeyboardButton("« Back to Main Menu", callback_data="main_menu")],
        ]
        await query.edit_message_text(
            "Frequently Asked Questions:\nSelect a topic below:",
            reply_markup=InlineKeyboardMarkup(faq_keyboard)
        )

    elif query.data == "faq_contact":
        text = "You can contact our support team directly via the 'Contact Support' button on the home screen."
        await query.edit_message_text(text=text, reply_markup=reply_markup)

    elif query.data == "faq_hours":
        text = "Our support team operates Monday through Friday, 09:00 - 18:00 UTC."
        await query.edit_message_text(text=text, reply_markup=reply_markup)

    elif query.data == "contact":
        text = (
            "📩 Support Channel:\n\n"
            "If you have inquiries, please leave a brief message, and our representative "
            "will respond within 24 hours."
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
