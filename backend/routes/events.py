from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.user import User, UserRole
from models.event import Event
from datetime import datetime

events_bp = Blueprint('events', __name__)

def is_admin(user_id):
    user = User.query.get(user_id)
    return user and user.role == UserRole.ADMIN

@events_bp.route('/', methods=['GET'])
def get_events():
    events = Event.query.order_by(Event.date.desc()).all()
    return jsonify([event.to_dict() for event in events]), 200

@events_bp.route('/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = Event.query.get_or_404(event_id)
    return jsonify(event.to_dict()), 200

@events_bp.route('/', methods=['POST'])
@jwt_required()
def create_event():
    user_id = int(get_jwt_identity())
    if not is_admin(user_id):
        return jsonify({'error': 'Admin access required'}), 403

    data = request.get_json()
    if not data.get('title') or not data.get('date'):
        return jsonify({'error': 'Title and date are required'}), 400

    event = Event(
        title=data['title'],
        description=data.get('description'),
        date=datetime.fromisoformat(data['date']),
        location=data.get('location'),
        image_url=data.get('image_url')
    )
    db.session.add(event)
    db.session.commit()
    return jsonify(event.to_dict()), 201
