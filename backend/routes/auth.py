from flask import Blueprint, request, jsonify, url_for
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from werkzeug.security import generate_password_hash
from models import db
from models.user import User
import re

auth_bp = Blueprint('auth', __name__)

# Configure serializer for password reset
serializer = URLSafeTimedSerializer("YOUR_SECRET_KEY_HERE")  # Replace with Config.SECRET_KEY if preferred

# -------------------------
# Validation helpers
# -------------------------
def validate_email(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

def validate_password(password):
    return len(password) >= 8

# -------------------------
# Register
# -------------------------
@auth_bp.route('/register/', methods=['POST'])
def register():
    data = request.get_json()
    required_fields = ['email', 'password', 'first_name', 'last_name']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400

    if not validate_email(data['email']):
        return jsonify({'error': 'Invalid email format'}), 400

    if not validate_password(data['password']):
        return jsonify({'error': 'Password must be at least 8 characters long'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'User already exists'}), 409

    user = User(
        email=data['email'],
        first_name=data['first_name'],
        last_name=data['last_name']
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

# -------------------------
# Login
# -------------------------
@auth_bp.route('/login/', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({
        'message': 'User logged in successfully',  # <-- Added this
        'access_token': access_token,
        'user': user.to_dict()
    }), 200

# -------------------------
# Request Password Reset
# -------------------------
@auth_bp.route('/request-password-reset/', methods=['POST'])
def request_password_reset():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    token = serializer.dumps(email, salt='password-reset-salt')
    reset_link = url_for('auth.reset_password', token=token, _external=True)

    # TODO: Replace this with actual email sending logic
    print(f"Password reset link: {reset_link}")

    return jsonify({'message': 'Password reset link has been sent to your email.'}), 200

# -------------------------
# Reset Password
# -------------------------
@auth_bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)  # 1-hour expiry
    except SignatureExpired:
        return jsonify({'error': 'The reset link has expired.'}), 400
    except BadSignature:
        return jsonify({'error': 'Invalid token.'}), 400

    data = request.get_json()
    new_password = data.get('password')

    if not new_password or not validate_password(new_password):
        return jsonify({'error': 'Password must be at least 8 characters long'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user.password = generate_password_hash(new_password)
    db.session.commit()

    return jsonify({'message': 'Password has been reset successfully.'}), 200
