import gspread
from google.oauth2.service_account import Credentials
import logging

# Google Sheets and Drive API Scopes
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

# Path to your Google service account credentials JSON file
CREDENTIALS_FILE = "credentials.json"
SHEET_NAME = "BI Code Team"

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def authenticate_google_sheets():
    """Authenticate with Google Sheets API using service account credentials."""
    try:
        # Authenticate using service account credentials
        credentials = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
        gc = gspread.authorize(credentials)
        logger.info("Successfully authenticated with Google Sheets.")
        return gc
    except Exception as e:
        logger.error(f"Authentication failed: {e}")
        raise

def save_to_sheets(data):
    """
    Append a new row with user data to the Google Sheets document.
    """
    try:
        gc = authenticate_google_sheets()
        worksheet = gc.open(SHEET_NAME).sheet1
        worksheet.append_row([
            data.get('name', ''),
            data.get('surname', ''),
            data.get('student_id', ''),
            data.get('contact', ''),
            data.get('payment_method', '')
        ])
        logger.info("Data successfully appended to Google Sheets.")
    except Exception as e:
        logger.error(f"Failed to save data to Google Sheets: {e}")
