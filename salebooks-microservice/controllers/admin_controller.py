from flask import Blueprint, render_template, redirect, url_for, flash, session, current_app
import requests
from utils.utils import check_user_auth

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
    
    headers = {'Authorization': f'Bearer {session.get("token")}'}
    response = requests.get(f'{current_app.config["AUTH_SERVICE_URL"]}/admin/users', headers=headers)
    if response.ok:
        users = response.json()
        return render_template('list_users.html', users=users, my_user=user)
    else:
        flash('Error fetching users. Please try again.', 'error')
        return redirect(url_for('home'))
    
