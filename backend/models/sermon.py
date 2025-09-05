from models import db
from datetime import datetime

class Sermon(db.Model):
    __tablename__ = 'sermons'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    preacher = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text)
    audio_url = db.Column(db.String(255))  # Optional
    scripture = db.Column(db.String(255))  # <-- Added this line

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "preacher": self.preacher,
            "date": self.date.isoformat(),
            "description": self.description,
            "audio_url": self.audio_url,
            "scripture": self.scripture
        }
