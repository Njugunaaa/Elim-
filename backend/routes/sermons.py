from flask import Blueprint, request, jsonify
from models import db
from models.sermon import Sermon

sermon_bp = Blueprint('sermons', __name__)

# Create a new sermon
@sermon_bp.route('/', methods=['POST'])
def create_sermon():
    data = request.get_json()
    required_fields = ['title', 'preacher']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400

    sermon = Sermon(
        title=data['title'],
        preacher=data['preacher'],
        description=data.get('description'),
        audio_url=data.get('audio_url')
    )
    db.session.add(sermon)
    db.session.commit()

    return jsonify({"message": "Sermon created successfully", "sermon": sermon.serialize()}), 201

# Get all sermons
@sermon_bp.route('/', methods=['GET'])
def get_sermons():
    sermons = Sermon.query.all()
    return jsonify([s.serialize() for s in sermons]), 200

# Get single sermon
@sermon_bp.route('/<int:id>', methods=['GET'])
def get_sermon(id):
    sermon = Sermon.query.get(id)
    if not sermon:
        return jsonify({"error": "Sermon not found"}), 404
    return jsonify(sermon.serialize()), 200

# Update sermon
@sermon_bp.route('/<int:id>', methods=['PUT'])
def update_sermon(id):
    sermon = Sermon.query.get(id)
    if not sermon:
        return jsonify({"error": "Sermon not found"}), 404

    data = request.get_json()
    sermon.title = data.get('title', sermon.title)
    sermon.preacher = data.get('preacher', sermon.preacher)
    sermon.description = data.get('description', sermon.description)
    sermon.audio_url = data.get('audio_url', sermon.audio_url)

    db.session.commit()
    return jsonify({"message": "Sermon updated successfully", "sermon": sermon.serialize()}), 200

# Delete sermon
@sermon_bp.route('/<int:id>', methods=['DELETE'])
def delete_sermon(id):
    sermon = Sermon.query.get(id)
    if not sermon:
        return jsonify({"error": "Sermon not found"}), 404

    db.session.delete(sermon)
    db.session.commit()
    return jsonify({"message": "Sermon deleted successfully"}), 200
