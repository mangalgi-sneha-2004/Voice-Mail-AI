import sys
sys.path.append(r"C:\Users\msneh\OneDrive\Desktop\mcp_agent")
import asyncio
import os
import edge_tts
from playsound import playsound
from config import TTS_MODE

async def speak_edge(text: str):
    communicate = edge_tts.Communicate(text, voice="en-US-GuyNeural")
    filename = "response.mp3"
    await communicate.save(filename)
    playsound(filename)
    os.remove(filename)

async def speak(text: str):
    if TTS_MODE == "edge":
        await speak_edge(text)

def say(text: str):
    asyncio.run(speak(text))

if __name__ == "__main__":
    say("Hello! I am your AI voice assistant. I am working perfectly!")