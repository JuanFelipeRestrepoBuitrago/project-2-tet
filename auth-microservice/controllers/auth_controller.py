from flask import Blueprint, request, jsonify
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from models.user import User
from extensions import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    """
    Handle login logic: validate user credentials and returns message.
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400
    
    user = User.query.filter_by(email=email).first()
    
    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({'message': 'Login successful', 'user': {'id': user.id, 'name': user.name, 'email': user.email}}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401
    


@auth.route('/register', methods=['POST'])
def register():
    """
    Handle user registration: create new user with hashed password.
    """
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
    return {'message': 'User registered successfully', 'user_id': new_user.id}, 201


@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    """
    Log out the current user and redirect to the login page.
    """
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200
