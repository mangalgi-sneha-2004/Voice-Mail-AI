from dotenv import load_dotenv
import os
load_dotenv()
GROQ_API_KEY=os.getenv("GROQ_API_KEY")
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
GMAIL_USER=os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD=os.getenv("GMAIL_APP_PASSWORD")
TTS_MODE=os.getenv("TTS_MODE","edge")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")