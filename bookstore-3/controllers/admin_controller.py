from flask import Blueprint, render_template, session, redirect, url_for
from utils.utils import check_user_auth
from models.user import User

admin = Blueprint('admin', __name__)

@admin.route('/admin/users')
def list_users():
    """
    Render the user list page for admin view.
    Only accessible to authenticated users.
    """
    user = check_user_auth(session.get('token'))
    if not user:
        return redirect(url_for('home'))
    users = User.query.all()
    return render_template('list_users.html', users=users, my_user=user)
