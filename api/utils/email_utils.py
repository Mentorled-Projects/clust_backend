import smtplib
from email.message import EmailMessage
from core.config.settings import settings
import traceback

def send_email_reminder(to_email: str, subject: str, content: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.MAIL_FROM or settings.EMAILS_FROM_EMAIL or "no-reply@example.com"
    msg["To"] = to_email
    msg.set_content(content)

    try:
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
            server.send_message(msg)
            print("✅ Email sent successfully.")
    except Exception as e:
        print(f"MAIL_USERNAME: {settings.MAIL_USERNAME}")
        print(f"MAIL_PASSWORD: {settings.MAIL_PASSWORD}")
        print(f"SMTP_SERVER: {settings.SMTP_SERVER}")
        print(f"SMTP_PORT: {settings.SMTP_PORT}")

        print(f"❌ Failed to send email: {e}")
        traceback.print_exc()
        raise
