import os
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from config.settings import CALENDAR_ID

# Load credentials
SERVICE_ACCOUNT_FILE = os.path.join(os.getcwd(), 'service_account.json')
SCOPES = ['https://www.googleapis.com/auth/calendar']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# Main function to create the event
def create_event(summary, start_datetime_str, duration_minutes=60):
    service = build('calendar', 'v3', credentials=credentials)

    # Parse start datetime
    start_datetime = datetime.datetime.fromisoformat(start_datetime_str)
    end_datetime = start_datetime + datetime.timedelta(minutes=duration_minutes)

    event = {
        'summary': summary,
        'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_datetime.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
    }

    # Actually insert the event
    event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()

    # ✅ Debug print to see EXACT Google response
    print("✅ GOOGLE EVENT RESPONSE:", event)

    return event.get('htmlLink')
