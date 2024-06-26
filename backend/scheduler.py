import schedule
import time
from datetime import datetime, timedelta
import sys
import os
import threading

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend import create_app
from backend.models import db, Event, Notification
from backend.email_service import send_email

app = create_app()

def send_weekly_automatic_exercise_email():
    with app.app_context():
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=4)

        events = Event.query.filter(
            Event.date >= start_of_week.date(),
            Event.date <= end_of_week.date(),
            Event.tags.contains('automatic exercise')
        ).all()

        if events:
            email_body = "Dear customer,\n\nWe would like to inform you about the following automatic exercises at B3 this week:\n\n"
            for event in events:
                email_body += f">>> {event.title} on {event.date.strftime('%Y-%m-%d')}\n\n      {event.description}\n\n"

            email_body += "\n\nBest regards and good trading,\nHFT Team of Nova Futura Investimentos."

            send_email(
                "Upcoming Automatic Exercise Events at B3",
                email_body,
                "pedro.faria@novafutura.com.br"
            )

def send_notifications():
    with app.app_context():
        notifications = Notification.query.all()
        for notification in notifications:
            send_email(notification.subject, notification.message, "recipient@example.com")

def run_scheduler():
    schedule.every().monday.at("08:00").do(send_weekly_automatic_exercise_email)

    while True:
        schedule.run_pending()
        time.sleep(1)

def start_scheduler_thread():
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

if __name__ == "__main__":
    start_scheduler_thread()
    app.run(debug=True)
