# Voice Mail AI


Speak one sentence. agent searches the web, finds your contact, and sends the email.

How it works:


Listens to your voice command

Searches the web for relevant information

Looks up the recipient from your contacts by name

Drafts and sends a personalized email

Speaks back a confirmation

Tools:


STT — Groq API (Whisper-v3) — fast, free, no local model needed

Brain — Gemini 2.5 Flash with OpenRouter fallback (LLaMA 3.3 70B)

TTS — Edge-TTS (Microsoft neural voices, free, no API key)

Tool Orchestration — FastMCP (Model Context Protocol)

Project structure:

voicemail-ai/
├── main.py              #Full conversation loop
├── agent.py             # LLM reasoning + tool-calling loop
├── mcp_server.py        # Registers tools via FastMCP
├── config.py            # Loads api's from .env
├── contacts.csv         
├── voice/
│   ├── stt.py           # Speech to text
│   └── tts.py           # Text to speech
└── tools/
    ├── search_tool.py   # Web search
    ├── email_tool.py    # Email sending
    └── contact_tool.py  # Contact lookup + disambiguation



Web Search — Answer API (free, no key)

Email — Gmail SMTP

Contacts — pandas + CSV with smart name disambiguation
