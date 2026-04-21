import aiosmtplib
from email.mime.text import MIMEText
import os


async def send_email(to: str, subject: str, body: str):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = os.environ.get("SMTP_FROM", "no-reply@kutahyalilar.com")
    msg["To"] = to

    await aiosmtplib.send(
        msg,
        hostname=os.environ.get("SMTP_HOST", "mailhog"),
        port=int(os.environ.get("SMTP_PORT", "1025")),
    )


def log_sms(phone: str, message: str):
    print(f"[SMS STUB] Sending SMS to {phone}: {message}")
