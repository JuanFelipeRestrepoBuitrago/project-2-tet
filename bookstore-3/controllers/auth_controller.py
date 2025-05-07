from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
import requests
from utils.utils import check_user_auth

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle login logic: validate user credentials and redirect on success.
    """
    if check_user_auth(session.get('token')):
        return redirect(url_for('book.catalog'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        response = requests.post(f'{current_app.config["AUTH_SERVICE_URL"]}/login', json={
            'email': email,
            'password': password
        })
        
        if response.ok:
            data = response.json()
            session['token'] = data['token']
            print(f"User {data['user']['name']} logged in successfully.")
            return redirect(url_for('book.catalog'))
        else:
            flash('Login failed. Please check your credentials.', 'error')

    return render_template('login.html', my_user=None)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle user registration: create new user with hashed password.
    """
    if check_user_auth(session.get('token')):
        return redirect(url_for('home'))
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        response = requests.post(f'{current_app.config["AUTH_SERVICE_URL"]}/register', json={
            'name': name,
            'email': email,
            'password': password
        })
        if response.ok:
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(response.json()['error'], 'error')

    return render_template('register.html', my_user=None)

@auth.route('/logout')
def logout():
    """
    Log out the current user and redirect to the login page.
    """
    token = session.get('token')
    user = check_user_auth(token)
    if user:
        response = requests.post(f'{current_app.config["AUTH_SERVICE_URL"]}/logout', headers={
            'Authorization': f'Bearer {token}'
        })
        if response.ok:
            session.pop('token', None)
            flash('Logged out successfully.', 'success')
        else:
            flash('Logout failed. Please try again.', 'error')
        return redirect(url_for('auth.login'))
    else:
        flash('You are not logged in.', 'warning')
        return redirect(url_for('auth.login'))
    
