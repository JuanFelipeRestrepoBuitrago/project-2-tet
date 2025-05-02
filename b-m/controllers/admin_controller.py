from flask import Blueprint, render_template
from flask_login import login_required

from models.user import User

admin = Blueprint('admin', __name__)

@admin.route('/admin/users')
@login_required
def list_users():
    """
    Render the user list page for admin view.
    Only accessible to authenticated users.
    """
    users = User.query.all()
    return render_template('list_users.html', users=users)
