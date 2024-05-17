import schedule
import time
import threading
from datetime import datetime, timedelta
from backend.models import Event, Notification
from backend.email_service import send_email
import pythoncom

def send_weekly_automatic_exercise_email(app):
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

def send_notifications(app):
    with app.app_context():
        notifications = Notification.query.all()
        for notification in notifications:
            send_email(notification.subject, notification.message, "recipient@example.com")

def run_scheduler(app):
    pythoncom.CoInitialize()
    schedule.every().monday.at("07:30").do(send_weekly_automatic_exercise_email, app=app)

    while True:
        schedule.run_pending()
        time.sleep(1)
    pythoncom.CoUninitialize()

def start_scheduler_thread(app):
    scheduler_thread = threading.Thread(target=run_scheduler, args=(app,))
    scheduler_thread.daemon = True
    scheduler_thread.start()
