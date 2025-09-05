from flask import Blueprint, request, jsonify
from models import db, Sermon

sermon_bp = Blueprint('sermons', __name__, url_prefix='/api/sermons')

@sermon_bp.route('/', methods=['POST'])
def create_sermon():
    data = request.get_json()

    new_sermon = Sermon(
        title=data.get('title'),
        preacher=data.get('preacher'),
        date=data.get('date'),  # Or datetime.utcnow() if not provided
        description=data.get('description'),
        audio_url=data.get('audio_url'),
        scripture=data.get('scripture')  # <-- Added this
    )

    db.session.add(new_sermon)
    db.session.commit()
    return jsonify(new_sermon.serialize()), 201


@sermon_bp.route('/<int:id>', methods=['PUT'])
def update_sermon(id):
    sermon = Sermon.query.get_or_404(id)
    data = request.get_json()

    sermon.title = data.get('title', sermon.title)
    sermon.preacher = data.get('preacher', sermon.preacher)
    sermon.date = data.get('date', sermon.date)
    sermon.description = data.get('description', sermon.description)
    sermon.audio_url = data.get('audio_url', sermon.audio_url)
    sermon.scripture = data.get('scripture', sermon.scripture)  # <-- Added this

    db.session.commit()
    return jsonify(sermon.serialize())
