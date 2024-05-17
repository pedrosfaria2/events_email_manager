import schedule
import time
from datetime import datetime, timedelta
import sys
import os

# Adicione o caminho do backend ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend import create_app
from backend.models import db, Event, Notification
from backend.email_service import send_email

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

        for event in events:
            send_email(
                "Upcoming Automatic Exercise Event",
                f"Don't forget about the automatic exercise event: {event.title} on {event.date}!",
                "pedro.faria@novafutura.com.br"
            )

def send_notifications():
    with app.app_context():
        notifications = Notification.query.all()
        for notification in notifications:
            send_email(notification.subject, notification.message, "recipient@example.com")

app = create_app()

# Bloco para teste manual
if __name__ == "__main__":
    with app.app_context():
        send_weekly_automatic_exercise_email()
    
    # Loop do agendamento (descomente para executar o agendamento)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
