import requests
from flask import current_app


def check_user_auth(token: str) -> dict:
    """Check if user is logged in by verifying JWT"""
    if not token:
        return None
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(f'{current_app.config['AUTH_SERVICE_URL']}/check_login', headers=headers)
        if response.ok and response.json().get('is_authenticated'):
            return response.json()['user']
        return None
    except requests.RequestException:
        return None