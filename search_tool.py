import sys
sys.path.append(r"C:\Users\msneh\OneDrive\Desktop\mcp_agent")
import httpx

async def search(query: str) -> str:
    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_redirect": 1,
        "no_html": 1
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()
    
    result = data.get("AbstractText", "")
    if not result:
        result = data.get("Answer", "No results found.")
    return result

if __name__ == "__main__":
    import asyncio
    result = asyncio.run(search("what is artificial intelligence"))
    print(result)

