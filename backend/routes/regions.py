from flask import Blueprint, request, jsonify
from models import db
from models.church_structure import Region, Church

regions_bp = Blueprint('regions', __name__)

# Get all regions
@regions_bp.route('/', methods=['GET'])
def get_regions():
    regions = Region.query.all()
    return jsonify([r.to_dict() for r in regions]), 200

# Create a region
@regions_bp.route('/', methods=['POST'])
def create_region():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({"error": "Name is required"}), 400
    if Region.query.filter_by(name=name).first():
        return jsonify({"error": "Region already exists"}), 409
    region = Region(name=name)
    db.session.add(region)
    db.session.commit()
    return jsonify(region.to_dict()), 201

# Update region
@regions_bp.route('/<int:id>', methods=['PUT'])
def update_region(id):
    region = Region.query.get_or_404(id)
    data = request.get_json()
    region.name = data.get('name', region.name)
    db.session.commit()
    return jsonify(region.to_dict()), 200

# Delete region
@regions_bp.route('/<int:id>', methods=['DELETE'])
def delete_region(id):
    region = Region.query.get_or_404(id)
    db.session.delete(region)
    db.session.commit()
    return jsonify({"message": "Region deleted successfully"}), 200
