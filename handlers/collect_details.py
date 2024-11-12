from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from utils.google_sheets import save_to_sheets
from utils.language_data import LANGUAGES

COLLECT_DETAILS = 2  # Define the state for collecting details

async def collect_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_lang = context.user_data.get('language', 'English')  # Get user language (default to English)
    lang_data = LANGUAGES[user_lang]  # Get the language data for the user

    # Step 1: Collect name
    if 'name' not in context.user_data:
        context.user_data['name'] = update.message.text
        await update.message.reply_text(lang_data["enter_surname"])

    # Step 2: Collect surname
    elif 'surname' not in context.user_data:
        context.user_data['surname'] = update.message.text
        await update.message.reply_text(lang_data["enter_student_id"])

    # Step 3: Collect student ID
    elif 'student_id' not in context.user_data:
        context.user_data['student_id'] = update.message.text
        await update.message.reply_text(lang_data["enter_contact"])

    # Step 4: Collect contact number
    elif 'contact' not in context.user_data:
        context.user_data['contact'] = update.message.text
        payment_options = [['Cash', 'Visa/MasterCard', 'Uzcard']]
        await update.message.reply_text(
            lang_data["select_payment"],
            reply_markup=ReplyKeyboardMarkup(payment_options, one_time_keyboard=True)
        )

    # Step 5: Collect payment method
    elif 'payment_method' not in context.user_data:
        context.user_data['payment_method'] = update.message.text

        # Ensure that the payment method is valid
        if context.user_data['payment_method'] not in ['Cash', 'Visa/MasterCard', 'Uzcard']:
            await update.message.reply_text(lang_data["invalid_payment"])
            return COLLECT_DETAILS  # Stay in the current step if invalid payment method is entered

        # Save the collected data to Google Sheets
        save_to_sheets(context.user_data)

        # Send a thank you message
        await update.message.reply_text(lang_data["thank_you"])
        return ConversationHandler.END

    # If the flow is still in progress, return to the current step
    return COLLECT_DETAILS


# Optional: If you want to handle cancellation
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("The conversation has been canceled.")
    return ConversationHandler.END
