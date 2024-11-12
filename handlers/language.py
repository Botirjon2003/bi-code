from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from utils.language_data import LANGUAGES

MENU = 1

async def language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_lang = update.message.text.strip()  # Ensure there are no extra spaces

    # Validate the language selection
    if user_lang not in LANGUAGES:
        await update.message.reply_text(
            "Sorry, we don't support that language. Please choose a supported language: English, Русский, or O‘zbek."
        )
        return MENU  # Return to the menu step
    
    # Set the language for the user
    context.user_data['language'] = user_lang
    lang_data = LANGUAGES[user_lang]  # Get the selected language data

    # Main menu options
    menu_keyboard = [[lang_data["rest_api"]]]  # Add more options here if needed
    await update.message.reply_text(
        lang_data["main_menu"],  # Display the main menu
        reply_markup=ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True)
    )
    return MENU
