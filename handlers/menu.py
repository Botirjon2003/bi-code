from telegram import Update
from telegram.ext import ContextTypes
from utils.language_data import LANGUAGES

COLLECT_DETAILS = 2  # Define the state for collecting details
MENU = 1  # The state for menu (you may use this to return to the menu)

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get user language (default to 'English')
    user_lang = context.user_data.get('language', 'English')
    lang_data = LANGUAGES.get(user_lang, LANGUAGES['English'])  # Get corresponding language data
    
    # Handle the menu option: 'rest_api'
    if update.message.text == lang_data["rest_api"]:
        # Prompt the user for their name (assuming this is how it's structured in your language data)
        await update.message.reply_text(lang_data["enter_name"])  # Ask for user details
        return COLLECT_DETAILS  # Return the state to collect user details
    
    # Add more menu options if needed
    elif update.message.text == lang_data["another_option"]:
        # Handle another option (add more options as needed)
        await update.message.reply_text(lang_data["another_option_response"])
        return MENU  # Return to menu (or another state if needed)

    # If an unexpected message is received, reply with a message and return to MENU state
    else:
        await update.message.reply_text(lang_data["invalid_option"])  # Handle invalid input
        return MENU  # Return to the menu state for re-selection
