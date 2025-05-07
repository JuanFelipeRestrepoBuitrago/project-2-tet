from flask import Blueprint, jsonify
from models.user import User

admin = Blueprint('admin', __name__)

@admin.route('/admin/users', methods=['GET'])
def list_users():
    """
    Return the list of users for admin view.
    """
    try:
        users = User.query.all()
        return jsonify([{
            'id': user.id,
            'name': user.name,
            'email': user.email
        } for user in users])
    except Exception as e:
        return jsonify({'error': 'Failed to fetch users', 'details': str(e)}), 500
