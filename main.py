from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler
from handlers.start import start
from handlers.language import language_selection
from handlers.menu import menu
from handlers.collect_details import collect_details, cancel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# States for the conversation
LANGUAGE, MENU, COLLECT_DETAILS = range(3)

# Telegram Bot Token from .env file
TOKEN = os.getenv("BOT_TOKEN")

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # Define the conversation handler
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, language_selection)],
            MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, menu)],
            COLLECT_DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_details)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Add the conversation handler to the application
    application.add_handler(conversation_handler)

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
