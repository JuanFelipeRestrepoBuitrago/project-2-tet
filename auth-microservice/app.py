import os
from flask import Flask
from extensions import db
from controllers.auth_controller import auth
from controllers.admin_controller import admin
from config import config
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from sqlalchemy.exc import OperationalError, DatabaseError

def create_app(config_name=None):
    """Crea y configura la aplicación Flask"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
        
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/auth')
    
    return app

@retry(
    stop=stop_after_attempt(5),  # Retry 5 times
    wait=wait_exponential(multiplier=1, min=2, max=10),  # Wait 2s, 4s, 8s, 10s, 10s
    retry=retry_if_exception_type((OperationalError, DatabaseError)),  # Retry on connection errors
    reraise=True  # Reraise the last exception if retries fail
)
def initialize_database(app):
    """
    Inicializa la base de datos y los proveedores de entrega con reintentos
    """
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    app = create_app()
    try:
        initialize_database(app)
    except Exception as e:
        print(f"Failed to initialize database after retries: {e}")
        raise
    app.run(host="0.0.0.0", debug=True)