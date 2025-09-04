from flask import Blueprint, request, jsonify
from models import db
from models.church_structure import Church, Region

churches_bp = Blueprint('churches', __name__)

# Get all churches
@churches_bp.route('/', methods=['GET'])
def get_churches():
    churches = Church.query.all()
    return jsonify([c.to_dict() for c in churches]), 200

# Get single church
@churches_bp.route('/<int:id>', methods=['GET'])
def get_church(id):
    church = Church.query.get_or_404(id)
    return jsonify(church.to_dict()), 200

# Create church
@churches_bp.route('/', methods=['POST'])
def create_church():
    data = request.get_json()
    name = data.get('name')
    region_id = data.get('region_id')
    if not name or not region_id:
        return jsonify({"error": "Name and region_id are required"}), 400
    if not Region.query.get(region_id):
        return jsonify({"error": "Region not found"}), 404

    church = Church(
        name=name,
        address=data.get('address'),
        point_of_contact=data.get('point_of_contact'),
        phone=data.get('phone'),
        email=data.get('email'),
        region_id=region_id
    )
    db.session.add(church)
    db.session.commit()
    return jsonify(church.to_dict()), 201

# Update church
@churches_bp.route('/<int:id>', methods=['PUT'])
def update_church(id):
    church = Church.query.get_or_404(id)
    data = request.get_json()
    church.name = data.get('name', church.name)
    church.address = data.get('address', church.address)
    church.point_of_contact = data.get('point_of_contact', church.point_of_contact)
    church.phone = data.get('phone', church.phone)
    church.email = data.get('email', church.email)
    church.region_id = data.get('region_id', church.region_id)
    db.session.commit()
    return jsonify(church.to_dict()), 200

# Delete church
@churches_bp.route('/<int:id>', methods=['DELETE'])
def delete_church(id):
    church = Church.query.get_or_404(id)
    db.session.delete(church)
    db.session.commit()
    return jsonify({"message": "Church deleted successfully"}), 200
