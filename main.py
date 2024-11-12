from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler
from handlers.start import start
from handlers.language import language_selection
from handlers.menu import menu
from handlers.collect_details import collect_details, cancel
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# States for the conversation
LANGUAGE, MENU, COLLECT_DETAILS = range(3)

# Retrieve the bot token from the .env file
TOKEN = os.getenv("BOT_TOKEN")

def main():
    if not TOKEN:
        raise ValueError("Bot token not found. Please set BOT_TOKEN in your .env file.")

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
