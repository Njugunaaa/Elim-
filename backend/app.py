from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from models import db
from config import Config
from routes import all_blueprints  # This contains (blueprint, prefix) tuples

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS
    CORS(app)

    # Initialize extensions
    db.init_app(app)
    JWTManager(app)
    Migrate(app, db)

    # Register all blueprints dynamically
    for blueprint, prefix in all_blueprints:
        app.register_blueprint(blueprint, url_prefix=prefix)

    @app.route('/')
    def home():
        return {"message": "Church Management Backend is Live!"}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
