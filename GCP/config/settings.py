import os
from dotenv import load_dotenv

load_dotenv()

EURI_API_KEY = os.getenv("EURI_API_KEY")
LLM_API_URL = os.getenv("LLM_API_URL")
CALENDAR_ID = os.getenv("CALENDAR_ID")
