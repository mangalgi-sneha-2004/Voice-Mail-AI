import sys
sys.path.append(r"C:\Users\msneh\OneDrive\Desktop\mcp_agent")
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import GMAIL_USER, GMAIL_APP_PASSWORD


async def send_email(to: str, subject: str, body: str) -> str:
    msg = MIMEMultipart()
    msg["From"] = GMAIL_USER
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    try:
       with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, to, msg.as_string())
       return f"Email sent to {to} successfully."
    except Exception as e:
        return f"Failed to send email: {str(e)}"

if __name__ == "__main__":
    import asyncio
    result = asyncio.run(send_email(
        to="msneha3110@gmail.com",
        subject="Test from MCP Agent",
        body="Hello! This email was sent by my AI voice agent."
    ))
    print(result)