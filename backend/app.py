from flask import Blueprint, request, jsonify, send_from_directory, render_template
from datetime import datetime
from .models import db, Event, Notification

main = Blueprint('main', __name__)

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


@main.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    data = request.get_json()
    event = db.session.get(Event, event_id)  # Alterado para db.session.get
    if not event:
        return jsonify({'message': 'Event not found'}), 404

    event.title = data['title']
    event.description = data['description']
    event.date = datetime.strptime(data['date'], '%Y-%m-%d').date()  # Converter string para date
    event.start_time = data.get('startTime')
    event.end_time = data.get('endTime')
    event.tags = data.get('tags', '')

    db.session.commit()
    return jsonify({'message': 'Event updated successfully'}), 200

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
    events = Event.query.all()
    events_list = []
    for event in events:
        events_list.append({
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'date': event.date.strftime('%Y-%m-%d'),
            'startTime': event.start_time,  # Corrigido para startTime
            'endTime': event.end_time,      # Corrigido para endTime
            'tags': event.tags
        })
    return jsonify(events_list), 200

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
