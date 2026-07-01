import sys
sys.path.append(r"C:\Users\msneh\OneDrive\Desktop\mcp_agent")
import json
from openai import OpenAI
from config import OPENROUTER_API_KEY
from tools.search_tool import search
from tools.email_tool import send_email
from tools.contact_tool import find_contact, list_all_contacts, add_contact
import time

import time

async def run_agent(user_input: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]

    while True:
        response = None
        for attempt in range(3):
            try:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    tools=tools,
                )
                break
            except Exception as e:
                if attempt < 2:
                    print(f"⚠️ Rate limited, retrying in 30 seconds... (attempt {attempt + 1}/3)")
                    time.sleep(30)
                else:
                    return f"Sorry, the AI service is temporarily unavailable. Please try again in a minute."

        if response is None:
            return "Sorry, the AI service is temporarily unavailable. Please try again in a minute."

        message = response.choices[0].message

        if message.tool_calls:
            messages.append(message.model_dump())

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                print(f"Agent calling: {tool_name} with {tool_args}")

                tool_fn = TOOL_MAP.get(tool_name)

                if tool_fn is None:
                    tool_result = f"Error: tool '{tool_name}' not found."
                else:
                    try:
                        tool_result = await tool_fn(**tool_args)
                    except TypeError as e:
                        tool_result = f"Error calling {tool_name}: {str(e)}. Check the parameters provided."

                print(f"Tool result: {tool_result}")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(tool_result)
                })
        else:
            return message.content


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

MODEL =  "google/gemma-4-31b-it:free"

TOOL_MAP = {
    "web_search": search,
    "email": send_email,
    "lookup_contact": find_contact,
    "show_contacts": list_all_contacts,
    "save_contact": add_contact
}

tools = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for current information about any topic",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "email",
            "description": "Send an email to a recipient with subject and body",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {
                        "type": "string",
                        "description": "Recipient email address"
                    },
                    "subject": {
                        "type": "string",
                        "description": "Email subject line"
                    },
                    "body": {
                        "type": "string",
                        "description": "Email body content"
                    }
                },
                "required": ["to", "subject", "body"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lookup_contact",
            "description": "Find a contact's email address by their name only",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The contact's name to search for"
                    }
                },
                "required": ["name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "show_contacts",
            "description": "List all saved contacts with their names and emails",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_contact",
            "description": "Add a new contact with name, email, and optional phone number",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The contact's full name"
                    },
                    "email": {
                        "type": "string",
                        "description": "The contact's email address"
                    },
                    "phone": {
                        "type": "string",
                        "description": "The contact's phone number (optional)"
                    }
                },
                "required": ["name", "email"]
            }
        }
    }
]

SYSTEM_PROMPT = """You are a helpful voice assistant with access to tools.
You MUST use the available tools to take real actions - never just describe what you would do.
Always respond in English only, regardless of what language the user speaks in.

When the user asks to send an email to someone by name (not email address):
1. First call lookup_contact to get their email address
2. Then call the email tool to ACTUALLY SEND the email
3. Confirm briefly: "Email sent to [name]"

When the user asks to research something and email it:
1. Call web_search to get information
2. Call the email tool with that information as the body - actually send it
3. Confirm what was sent

Keep all responses under 3 sentences since they will be spoken out loud.
Never read out long email content - just confirm the action taken."""


async def run_agent(user_input: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]
    FALLBACK_MODELS = [
    "google/gemma-4-31b-it:free",
    "qwen/qwen3-coder:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    
]

    while True:
        response = None
        for model_name in FALLBACK_MODELS:
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    tools=tools,
                )
                break
            except Exception as e:
                print(f"⚠️ {model_name} unavailable ({str(e)[:80]}), trying next model...")
                continue

        if response is None:
            return "Sorry, all AI services are temporarily unavailable. Please try again shortly."

        message = response.choices[0].message

        if message.tool_calls:
            messages.append(message.model_dump())

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                print(f"Agent calling: {tool_name} with {tool_args}")

                tool_fn = TOOL_MAP.get(tool_name)

                if tool_fn is None:
                    tool_result = f"Error: tool '{tool_name}' not found."
                else:
                    try:
                        tool_result = await tool_fn(**tool_args)
                    except TypeError as e:
                        tool_result = f"Error calling {tool_name}: {str(e)}. Check the parameters provided."

                print(f"Tool result: {tool_result}")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(tool_result)
                })
        else:
            return message.content


if __name__ == "__main__":
    import asyncio
    result = asyncio.run(run_agent(
        "search for latest AI trends and tell me a brief summary"
    ))
    print(f"Agent response: {result}")