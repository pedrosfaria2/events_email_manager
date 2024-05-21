from flask import Blueprint, request, jsonify, send_from_directory, render_template, url_for
from datetime import datetime, timedelta
from .models import db, Event, Notification, EmailLog
import react
import os
from bs4 import BeautifulSoup
from sqlalchemy import desc
import win32com.client
import pythoncom
from .email_checker import check_emails, send_saved_email

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

main = Blueprint('main', __name__)

@main.route('/send_email/<int:email_id>', methods=['POST'])
def send_email(email_id):
    try:
        send_saved_email(email_id)
        return jsonify({'message': 'Email sent successfully'}), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': f'Failed to send email: {str(e)}'}), 500

@main.route('/email_logs', methods=['GET'])
def fetch_email_logs():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    query_term = request.args.get('query')

    query = EmailLog.query.order_by(desc(EmailLog.id))

    if start_date:
        start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        query = query.filter(EmailLog.date_sent >= start_datetime)
    if end_date:
        # Adicionando 1 dia à data final para considerar o intervalo completo do último dia
        end_datetime = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
        query = query.filter(EmailLog.date_sent <= end_datetime)
    if query_term:
        query = query.filter(
            (EmailLog.subject.ilike(f'%{query_term}%'))
        )

    email_logs = query.all()

    email_logs_list = [
        {
            'id': log.id,
            'subject': log.subject,
            'date_sent': log.date_sent.strftime('%Y-%m-%d %H:%M:%S'),
            'html_file': log.html_file
        } for log in email_logs
    ]
    return jsonify(email_logs_list)

@main.route('/email_logs/<int:email_id>', methods=['GET'])
def get_email_log(email_id):
    email_log = EmailLog.query.get(email_id)
    if not email_log:
        return jsonify({'message': 'Email not found'}), 404

    email_path = os.path.join(BASE_DIR, 'emails/htmls', email_log.html_file)
    with open(email_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    images = soup.find_all('img')
    for img in images:
        src = img.get('src')
        if src and src.startswith('cid:'):
            cid = src[4:]
            img['src'] = f'/emails/attachments/{cid}.png'

    return str(soup)

@main.route('/view_emails.html')
def view_emails_page():
    return render_template('view_emails.html')

@main.route('/reset_email_logs', methods=['POST'])
def reset_email_logs():
    try:
        # Drop the table
        EmailLog.__table__.drop(db.engine)
        # Recreate the table
        db.create_all()
        return jsonify({'status': 'success', 'message': 'EmailLog table reset successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@main.route('/email_logs', methods=['GET'])
def get_email_logs():
    email_logs = EmailLog.query.all()
    email_logs_list = [
        {
            'id': log.id,
            'subject': log.subject,
            'date_sent': log.date_sent.strftime('%Y-%m-%d %H:%M:%S'),
            'html_file': log.html_file
        } for log in email_logs
    ]
    return jsonify(email_logs_list)

@main.route('/list_tables')
def list_tables():
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    return jsonify(tables)

@main.route('/manage_scheduled_jobs.html')
def manage_scheduled_jobs():
    return render_template('manage_scheduled_jobs.html')

@main.route('/send_events', methods=['POST'])
def send_events():
    data = request.get_json()
    event_ids = data.get('event_ids', [])

    if not event_ids:
        return jsonify({'message': 'No event IDs provided.'}), 400

    events = Event.query.filter(Event.id.in_(event_ids)).all()
    if not events:
        return jsonify({'message': 'No events found.'}), 404

    event_data = []
    for event in events:
        event_data.append({
            'title': event.title,
            'description': event.description,
            'date': event.date.strftime('%Y-%m-%d'),
            'startTime': event.start_time,
            'endTime': event.end_time,
            'tags': event.tags
        })

    return jsonify({'subject': 'Important B3 Events', 'events': event_data}), 200


@main.route('/events/<int:event_id>', methods=['PATCH', 'PUT'])
def update_event(event_id):
    data = request.get_json()
    event = db.session.get(Event, event_id)
    if event is None:
        return jsonify({"message": "Event not found"}), 404
    
    if request.method == 'PATCH':
        if 'title' in data:
            event.title = data['title']
        if 'description' in data:
            event.description = data['description']
        if 'date' in data:
            event.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        if 'startTime' in data:
            event.start_time = data['startTime']
        if 'endTime' in data:
            event.end_time = data['endTime']
        if 'tags' in data:
            event.tags = data['tags']
    else:
        event.title = data['title']
        event.description = data['description']
        event.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        event.start_time = data['startTime']
        event.end_time = data['endTime']
        event.tags = data['tags']

    db.session.commit()
    return jsonify({"message": "Event updated successfully"})


@main.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = db.session.get(Event, event_id)  # Alterado para db.session.get
    if not event:
        return jsonify({'message': 'Event not found'}), 404

    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted successfully'}), 200

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/index.html')
def index1():
    return render_template('index.html')

@main.route('/static/<path:path>')
def static_files(path):
    return send_from_directory('../frontend/static', path)

@main.route('/manage_events.html')
def manage_events():
    return render_template('manage_events.html')

@main.route('/add_event.html')
def add_event_page():
    return render_template('add_event.html')

@main.route('/check_events.html')
def check_event_page():
    return render_template('check_events.html')

@main.route('/send_events.html')
def send_events_page():
    return render_template('send_events.html')

@main.route('/events', methods=['POST'])
def add_event():
    data = request.get_json()
    if 'title' not in data or 'date' not in data:
        return {"error": "title and date are required fields"}, 400  # Bad Request

    event = Event(
        title=data['title'],
        description=data['description'],
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),  # Converter string para date
        start_time=data.get('startTime'),
        end_time=data.get('endTime'),
        tags=data.get('tags', '')
    )
    db.session.add(event)
    db.session.commit()
    return jsonify({'message': 'Event added successfully'}), 201

@main.route('/events', methods=['GET'])
def get_events():
    start_date_str = request.args.get('start')
    end_date_str = request.args.get('end')

    if start_date_str and end_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        events = Event.query.filter(Event.date >= start_date, Event.date <= end_date).all()
    else:
        events = Event.query.all()

    events_list = []
    for event in events:
        events_list.append({
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'date': event.date.strftime('%Y-%m-%d'),
            'startTime': event.start_time,
            'endTime': event.end_time,
            'tags': event.tags
        })

    return jsonify(events_list)

@main.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = db.session.get(Event, event_id)  # Alterado para db.session.get
    if not event:
        return jsonify({'message': 'Event not found'}), 404

    event_data = {
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'date': event.date.strftime('%Y-%m-%d'),
        'startTime': event.start_time,  # Corrigido para startTime
        'endTime': event.end_time,      # Corrigido para endTime
        'tags': event.tags
    }
    return jsonify(event_data), 200

@main.route('/notifications', methods=['POST'])
def add_notification():
    data = request.get_json()
    notification = Notification(subject=data['subject'], message=data['message'])
    db.session.add(notification)
    db.session.commit()
    return jsonify({'message': 'Notification added successfully'}), 201

@main.route('/notifications', methods=['GET'])
def get_notifications():
    notifications = Notification.query.all()
    notifications_list = [{'subject': n.subject, 'message': n.message} for n in notifications]
    return jsonify(notifications_list), 200
