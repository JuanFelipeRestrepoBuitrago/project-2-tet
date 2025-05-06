from flask import Blueprint, request, jsonify, current_app
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from extensions import db
import datetime
import jwt

auth = Blueprint('auth', __name__)

def generate_jwt(user_id, email, name):
    """Generate a JWT for the user"""
    payload = {
        'user_id': user_id,
        'email': email,
        'name': name,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),  # Token expires in 24 hours
        'iat': datetime.datetime.utcnow()
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

@auth.route('/login', methods=['POST'])
def login():
    """
    Handle login logic: validate user credentials and returns message.
    """
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Missing required fields'}), 400

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            token = generate_jwt(user.id, user.email, user.name)
            return jsonify({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email
                },
                'token': token
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': 'Login failed', 'details': str(e)}), 500

@auth.route('/register', methods=['POST'])
def register():
    """
    Handle user registration: create new user with hashed password.
    """
    try:
        data = request.get_json()
        email = data.get('email')
        name = data.get('name')
        password = data.get('password')

        if not email or not name or not password:
            return jsonify({'error': 'Missing required fields'}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 400

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed', 'details': str(e)}), 500

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    """
    Log out the current user.
    """
    try:
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'No token provided'}), 401
        if token.startswith('Bearer '):
            token = token.split(' ')[1]

        jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return jsonify({'message': 'Logout successful, please clear the token'}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token already expired, please clear it'}), 200
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    except Exception as e:
        return jsonify({'error': 'Logout failed', 'details': str(e)}), 500
    

@auth.route('/check_login', methods=['GET'])
def check_login():
    """
    Check if a user is logged in and return user details if authenticated.
    """
    try:
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'is_authenticated': False, 'message': 'No token provided'}), 401
        
        if token.startswith('Bearer '):
            token = token.split(' ')[1]
        
        payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return jsonify({
            'is_authenticated': True,
            'user': {
                'id': payload['user_id'],
                'name': payload['name'],
                'email': payload['email']
            }
        }), 200
        
    except jwt.ExpiredSignatureError:
        return jsonify({'is_authenticated': False, 'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'is_authenticated': False, 'message': 'Invalid token'}), 401
    except Exception as e:
        return jsonify({'is_authenticated': False, 'message': 'Token validation failed', 'details': str(e)}), 500