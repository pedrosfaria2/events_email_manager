from flask import Blueprint, request, jsonify, send_from_directory
from datetime import datetime
from .models import db, Event, Notification

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@main.route('/<path:path>')
def static_files(path):
    return send_from_directory('../frontend/static', path)

@main.route('/events', methods=['POST'])
def add_event():
    data = request.get_json()
    event = Event(title=data['title'], description=data['description'], date=datetime.strptime(data['date'], '%Y-%m-%d'))
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
    events_list = [{'title': e.title, 'description': e.description, 'date': e.date.strftime('%Y-%m-%d')} for e in events]
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
