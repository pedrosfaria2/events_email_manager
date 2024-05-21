import schedule
import time as pytime
import threading
from datetime import datetime, timedelta
from .models import Event, Notification
from .email_service import send_email
from .email_checker import check_emails
import pythoncom

disabled_jobs = set()
job_registry = {}
job_counter = 1

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
            send_email(notification.subject, notification.message, "")

def run_scheduler(app):
    pythoncom.CoInitialize()
    global job_counter
    
    job1 = schedule.every().monday.at("07:30").do(send_weekly_automatic_exercise_email, app=app)
    job_registry[job_counter] = {
        'job': job1,
        'name': 'send_weekly_automatic_exercise_email',
        'frequency': 'every monday',
        'time': '07:30'
    }
    job_counter += 1
    
    job2 = schedule.every(1).seconds.do(check_emails, app=app)  # Verificação de e-mails a cada 10 minutos
    job_registry[job_counter] = {
        'job': job2,
        'name': 'check_emails',
        'frequency': 'every 1 seconds',
        'time': 'N/A'
    }
    job_counter += 1

    while True:
        schedule.run_pending()
        pytime.sleep(1)
    pythoncom.CoUninitialize()

def start_scheduler_thread(app):
    scheduler_thread = threading.Thread(target=run_scheduler, args=(app,))
    scheduler_thread.daemon = True
    scheduler_thread.start()

def get_scheduled_jobs():
    jobs = []
    for job_id, job_info in job_registry.items():
        job = job_info['job']
        jobs.append({
            'id': job_id,
            'name': job_info['name'],
            'frequency': job_info['frequency'],
            'time': job_info['time'],
            'enabled': job_id not in disabled_jobs
        })
    return jobs

def enable_job(job_id):
    disabled_jobs.discard(job_id)

def disable_job(job_id):
    disabled_jobs.add(job_id)
