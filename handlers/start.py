from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from utils.language_data import LANGUAGES  # Ensure this is imported properly

CHANNEL_USERNAME = "@bi_code_team"
LANGUAGE = 0  # Conversation state for language selection

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    try:
        # Checking if the user is a member of the channel
        member_status = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user.id)
        if member_status.status not in ['member', 'administrator', 'creator']:
            await update.message.reply_text(f"Please subscribe to our channel {CHANNEL_USERNAME} to use the bot.")
            return ConversationHandler.END
    except telegram.error.BadRequest as e:
        # Handle errors specific to Telegram's API
        await update.message.reply_text("Error checking subscription. Please contact support.")
        print(f"BadRequest error: {e}")
        return ConversationHandler.END
    except Exception as e:
        # General error handling
        await update.message.reply_text("An unexpected error occurred. Please try again later.")
        print(f"Unexpected error: {e}")
        return ConversationHandler.END

    # Prompt user to select a language
    language_keyboard = [['English', 'Русский', 'O‘zbek']]
    await update.message.reply_text(
        LANGUAGES["English"]["select_language"],  # Assuming LANGUAGES dictionary is correctly structured
        reply_markup=ReplyKeyboardMarkup(language_keyboard, one_time_keyboard=True)
    )
    return LANGUAGE  # Return the state for further processing (language selection)
