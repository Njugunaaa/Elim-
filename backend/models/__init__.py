# backend/models/__init__.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .event import Event
from .sermon import Sermon
from .church_structure import Region, Church, Ministry

