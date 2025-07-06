import requests
from config.settings import EURI_API_KEY, LLM_API_URL
from app.google_calendar import create_event
import re
import datetime

# --- Helper: parse_booking_details ---
def parse_booking_details(user_message):
    """
    Very basic parser to extract date, time, and description.
    Example expected input:
        "Book appointment on 10-08-2025 at 10 PM to go to the hospital"
    """
    date_match = re.search(r"(\d{2}-\d{2}-\d{4})", user_message)
    time_match = re.search(r"(\d{1,2}(?::\d{2})?\s*(?:AM|PM|am|pm))", user_message)
    description_match = re.search(r"to (.+)$", user_message)

    date_str = date_match.group(1) if date_match else None
    time_str = time_match.group(1) if time_match else "10:00 AM"
    description = description_match.group(1) if description_match else "General Appointment"

    if not date_str:
        raise ValueError("❌ Could not find a date in your message. Please say 'on DD-MM-YYYY'.")

    try:
        dt_obj = datetime.datetime.strptime(f"{date_str} {time_str}", "%d-%m-%Y %I %p")
    except ValueError:
        dt_obj = datetime.datetime.strptime(f"{date_str} 10:00 AM", "%d-%m-%Y %I %p")

    return {
        "start_datetime": dt_obj.isoformat(),
        "description": description
    }

# --- Main booking function ---
def book_appointment(user_message):
    """
    Creates a real Google Calendar event.
    """
    try:
        details = parse_booking_details(user_message)
        link = create_event(
            summary=f"Appointment: {details['description']}",
            start_datetime_str=details['start_datetime']
        )
        return (
            f"✅ Your appointment has been booked!\n\n"
            f"📅 When: {details['start_datetime']}\n"
            f"📌 Link: [View Event]({link})"
        )
    except Exception as e:
        return f"⚠️ Failed to book appointment: {e}"

# --- EURI LLM Integration ---
def get_response(chat_history):
    """
    Calls EURI chat completions API.
    Uses only the last user message for context.
    Includes a SYSTEM prompt so the assistant behaves.
    """
    if not EURI_API_KEY or not LLM_API_URL:
        return "❌ Error: Missing EURI_API_KEY or LLM_API_URL in .env"

    user_input = chat_history[-1]["content"]

    headers = {
        "Authorization": f"Bearer {EURI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an appointment booking assistant. "
                    "When a user asks to book an appointment, clearly confirm the date, time, and purpose they gave you. "
                    "Say: 'Sure, I will book this appointment for you.'"
                )
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        "model": "gpt-4.1-nano",
        "max_tokens": 1000,
        "temperature": 0.7
    }

    try:
        response = requests.post(LLM_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        print("✅ Raw EURI response:", data)  # Debugging log

        # Handle both possible API response shapes
        choices = (
            data.get("choices")
            or data.get("data", {}).get("choices")
            or []
        )

        if not choices:
            return f"❌ Error: No assistant response found.\nFull API response:\n{data}"

        assistant_reply = choices[0]["message"]["content"]
        print("✅ Assistant Raw Reply:", assistant_reply)  # Debugging log

        # Very simple intent detection
        if "book" in assistant_reply.lower() and "appointment" in assistant_reply.lower():
            booking_confirmation = book_appointment(user_input)
            return f"{assistant_reply}\n\n{booking_confirmation}"

        return assistant_reply

    except Exception as e:
        return f"❌ Error calling EURI API: {e}"
