import schedule
import time
from backend.email_service import send_email
from backend.models import db, Event, Notification

def send_weekly_event_emails():
    events = Event.query.all()
    for event in events:
        send_email("Upcoming Event", f"Don't forget about {event.title} on {event.date}!", "recipient@example.com")

def send_notifications():
    notifications = Notification.query.all()
    for notification in notifications:
        send_email(notification.subject, notification.message, "recipient@example.com")

schedule.every().monday.at("08:00").do(send_weekly_event_emails)
schedule.every().day.at("09:00").do(send_notifications)

while True:
    schedule.run_pending()
    time.sleep(1)
