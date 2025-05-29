from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from core.config.settings import settings
import traceback
from pydantic import EmailStr

def send_email_reminder(to_email: str, subject: str, content: str):
    from_email = settings.MAIL_FROM or settings.EMAILS_FROM_EMAIL or "no-reply@example.com"

    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=content
    )

    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print("✅ Email sent successfully.")
        return response.status_code
    except Exception as e:
        print(f"❌ Failed to send email via SendGrid: {e}")
        traceback.print_exc()
        raise
