from .auth import auth_bp
from .events import events_bp
from .user import user_bp
from .sermons import sermon_bp
from .regions import regions_bp
from .churches import churches_bp
from .ministries import ministries_bp


all_blueprints = [
    (auth_bp, "/api/auth"),
    (events_bp, "/api/events"),
    (user_bp, "/api/users"),
    (sermon_bp, "/api/sermons"),
    (regions_bp, "/api/regions"),
    (churches_bp, "/api/churches"),
    (ministries_bp, "/api/ministries"),
]
