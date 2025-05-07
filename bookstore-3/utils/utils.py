import requests
from flask import current_app


def check_user_auth(token):
    """
    Verifica si el token de usuario es válido haciendo una petición al microservicio de autenticación.
    """
    if not token:
        return None
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f"{current_app.config['AUTH_SERVICE_URL']}/check_login", headers=headers)
    
    if response.ok:
        return response.json()
    return None