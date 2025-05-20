from celery import Celery
from api.utils.email_utils import send_email_reminder

celery = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery.task
def schedule_event_reminder(to_email: str, event_title: str, event_time: str):
    subject = f"Reminder: Upcoming Event - {event_title}"
    content = f"Hi there,\n\nThis is a reminder that your event '{event_title}' starts at {event_time}.\n\nSee you there!"
    send_email_reminder(to_email, subject, content)
