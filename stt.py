import sys
sys.path.append(r"C:\Users\msneh\OneDrive\Desktop\mcp_agent")
import os
import  numpy as np
import wave
import tempfile
from groq import Groq
from config import  GROQ_API_KEY
import sounddevice as sd
client=Groq(api_key=GROQ_API_KEY)
def record_audio(duration=20,sample_rate=16000):
    print(f"Listening for {duration} seconds... Speak now!")
    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype=np.int16
    )
    sd.wait()
    print("Recording done!")
    return audio, sample_rate
def save_audio(audio,sample_rate):
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    with wave.open(tmp.name, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())
    return tmp.name
def transcribe(duration=5):
    audio, sr = record_audio(duration)
    filepath = save_audio(audio, sr)
    with open(filepath, "rb") as f:
        result = client.audio.transcriptions.create(
        model="whisper-large-v3",
        file=f,
        response_format="text",
        language="en"
    )
        
    os.remove(filepath)
    return result
if __name__ == "__main__":
    print("Starting test...")
    text = transcribe(duration=20)
    print(f"You said: {text}")

