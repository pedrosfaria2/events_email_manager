# backend/app.py

from flask import Blueprint, request, jsonify, send_from_directory, render_template
from datetime import datetime
from .models import db, Event, Notification

main = Blueprint('main', __name__)

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

@main.route('/events', methods=['POST'])
def add_event():
    data = request.get_json()
    event = Event(
        title=data['title'],
        description=data['description'],
        date=datetime.strptime(data['date'], '%Y-%m-%d').strftime('%Y-%m-%d'),
        start_time=data.get('startTime'),
        end_time=data.get('endTime'),
        recurrence=data.get('recurrence'),
        all_day=data.get('allDay', False)
    )
    db.session.add(event)
    db.session.commit()
    return jsonify({'message': 'Event added successfully'}), 201

@main.route('/events', methods=['GET'])
def get_events():
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        events = Event.query.filter(Event.date.between(start_date, end_date)).all()
    else:
        events = Event.query.all()
    
    events_list = [
        {
            'title': e.title,
            'description': e.description,
            'date': e.date,
            'start_time': e.start_time,
            'end_time': e.end_time,
            'recurrence': e.recurrence,
            'all_day': e.all_day
        } 
        for e in events
    ]
    return jsonify(events_list), 200

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
