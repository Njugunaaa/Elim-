from . import db
from datetime import datetime

# -------------------------
# Regions
# -------------------------
class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    churches = db.relationship('Church', backref='region', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "churches": [c.to_dict_basic() for c in self.churches]
        }

# -------------------------
# Churches
# -------------------------
class Church(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    point_of_contact = db.Column(db.String(100))  # e.g., pastor or admin
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
    ministries = db.relationship('Ministry', backref='church', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "point_of_contact": self.point_of_contact,
            "phone": self.phone,
            "email": self.email,
            "region": self.region.name if self.region else None,
            "ministries": [m.to_dict_basic() for m in self.ministries]
        }

    def to_dict_basic(self):
        return {"id": self.id, "name": self.name}

# -------------------------
# Ministries
# -------------------------
class Ministry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    church_id = db.Column(db.Integer, db.ForeignKey('church.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "church": self.church.name if self.church else None
        }

    def to_dict_basic(self):
        return {"id": self.id, "name": self.name}
