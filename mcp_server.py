import sys
sys.path.append(r"C:\Users\msneh\OneDrive\Desktop\mcp_agent")
from mcp.server.fastmcp import FastMCP
from tools.search_tool import search
from tools.email_tool import send_email
from tools.contact_tool import find_contact, list_all_contacts, add_contact

mcp = FastMCP("VoiceAgent")

@mcp.tool()
async def web_search(query: str) -> str:
    """Search the web for information about a topic."""
    return await search(query)

@mcp.tool()
async def email(to: str, subject: str, body: str) -> str:
    """Send an email to a recipient."""
    return await send_email(to, subject, body)
@mcp.tool()
async def lookup_contact(name: str) -> str:
    """Find a contact's email by name. If multiple matches exist, asks for clarification."""
    return await find_contact(name)

@mcp.tool()
async def show_contacts() -> str:
    """List all saved contacts."""
    return await list_all_contacts()

@mcp.tool()
async def save_contact(name: str, email: str, phone: str = "") -> str:
    """Add a new contact to the contacts list."""
    return await add_contact(name, email, phone)

if __name__ == "__main__":
    print("MCP Server running...")
    
    mcp.run()