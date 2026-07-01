import sys
sys.path.append(r"C:\Users\msneh\OneDrive\Desktop\mcp_agent")
import pandas as pd
import os

CONTACTS_FILE = "contacts.csv"

def ensure_contacts_file_exists():
    """Create contacts.csv with sample data if it doesn't exist yet."""
    if not os.path.exists(CONTACTS_FILE):
        sample_data = {
            "name": ["Sneha Mangalgi"],
            "email": ["msneha3110@gmail.com"]

        }
        df = pd.DataFrame(sample_data)
        df.to_csv(CONTACTS_FILE, index=False)


async def find_contact(name: str) -> str:
    ensure_contacts_file_exists()
    df = pd.read_csv(CONTACTS_FILE)

    search_words = name.lower().split()

    def matches_all_words(contact_name):
        contact_lower = contact_name.lower()
        return all(word in contact_lower for word in search_words)

    matches = df[df["name"].apply(matches_all_words)]

    if len(matches) == 0:
        return f"No contact found with the name '{name}'. Please check the spelling or add them to contacts.csv."
    elif len(matches) == 1:
        contact_name = matches.iloc[0]["name"]
        contact_email = matches.iloc[0]["email"]
        return f"Found contact: {contact_name} ({contact_email})"
    else:
        names_list = matches["name"].tolist()
        names_str = ", ".join(names_list)
        return f"Multiple contacts found matching '{name}': {names_str}. Please specify the full name."

async def get_contact_email(full_name: str) -> str:
    """
    Get the exact email for a full name match (used after disambiguation).
    """
    ensure_contacts_file_exists()
    df = pd.read_csv(CONTACTS_FILE)

    match = df[df["name"].str.lower() == full_name.lower()]

    if len(match) == 0:
        return f"No exact contact found for '{full_name}'."

    return match.iloc[0]["email"]


async def list_all_contacts() -> str:
    """Return all contacts as a readable list."""
    ensure_contacts_file_exists()
    df = pd.read_csv(CONTACTS_FILE)

    if len(df) == 0:
        return "No contacts found in contacts.csv"

    contact_lines = [f"{row['name']} - {row['email']}" for _, row in df.iterrows()]
    return "Contacts:\n" + "\n".join(contact_lines)


async def add_contact(name: str, email: str, phone: str = "") -> str:
    """Add a new contact to contacts.csv"""
    ensure_contacts_file_exists()
    df = pd.read_csv(CONTACTS_FILE)

    new_row = pd.DataFrame([{"name": name, "email": email}])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(CONTACTS_FILE, index=False)

    return f"Added {name} ({email}) to contacts."


if __name__ == "__main__":
    import asyncio

    print("Testing contacts tool...\n")

    # test 1: single match
    result = asyncio.run(find_contact("John"))
    print(f"Test 1 (single match): {result}\n")

    # test 2: this will show multiple matches if you add another 'Sneha'
    result = asyncio.run(find_contact("Sneha"))
    print(f"Test 2 (Sneha search): {result}\n")

    # test 3: no match
    result = asyncio.run(find_contact("Nobody"))
    print(f"Test 3 (no match): {result}\n")

    # test 4: list all
    result = asyncio.run(list_all_contacts())
    print(f"Test 4 (list all):\n{result}\n")