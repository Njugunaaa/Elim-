from flask import Blueprint, request, jsonify
from models import db
from models.church_structure import Ministry, Church

ministries_bp = Blueprint('ministries', __name__)

# Get all ministries
@ministries_bp.route('/', methods=['GET'])
def get_ministries():
    ministries = Ministry.query.all()
    return jsonify([m.to_dict() for m in ministries]), 200

# Create ministry
@ministries_bp.route('/', methods=['POST'])
def create_ministry():
    data = request.get_json()
    name = data.get('name')
    church_id = data.get('church_id')
    if not name or not church_id:
        return jsonify({"error": "Name and church_id are required"}), 400
    if not Church.query.get(church_id):
        return jsonify({"error": "Church not found"}), 404

    ministry = Ministry(name=name, description=data.get('description'), church_id=church_id)
    db.session.add(ministry)
    db.session.commit()
    return jsonify(ministry.to_dict()), 201

# Update ministry
@ministries_bp.route('/<int:id>', methods=['PUT'])
def update_ministry(id):
    ministry = Ministry.query.get_or_404(id)
    data = request.get_json()
    ministry.name = data.get('name', ministry.name)
    ministry.description = data.get('description', ministry.description)
    ministry.church_id = data.get('church_id', ministry.church_id)
    db.session.commit()
    return jsonify(ministry.to_dict()), 200

# Delete ministry
@ministries_bp.route('/<int:id>', methods=['DELETE'])
def delete_ministry(id):
    ministry = Ministry.query.get_or_404(id)
    db.session.delete(ministry)
    db.session.commit()
    return jsonify({"message": "Ministry deleted successfully"}), 200
