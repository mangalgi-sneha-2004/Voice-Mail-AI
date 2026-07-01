import sys
sys.path.append(r"C:\Users\msneh\OneDrive\Desktop\mcp_agent")
import asyncio
from voice.stt import transcribe
from voice.tts import speak
from agent import run_agent

async def main():
    print("\n" + "="*50)
    print("MCP VOICE AGENT STARTING")
    print("="*50 + "\n")

    await speak("Hello! I am your AI assistant. How can I help you today?")
    print("\n[AGENT FINISHED SPEAKING]\n")

    while True:
        print("-"*50)
        print(" LISTENING NOW — SPEAK YOUR COMMAND")
        print("-"*50)
        
        user_input = transcribe(duration=10)
        
        print(f"\n YOU SAID: {user_input}\n")

        if "exit" in user_input.lower() or "quit" in user_input.lower():
            await speak("Goodbye!")
            break

        print(" AGENT IS THINKING...\n")
        response = await run_agent(user_input)
        
        print(f"\n AGENT RESPONSE: {response}\n")
        
        print(" AGENT IS SPEAKING NOW...\n")
        await speak(response)
        print("\n[AGENT FINISHED SPEAKING — LISTENING AGAIN]\n")

if __name__ == "__main__":
    asyncio.run(main())