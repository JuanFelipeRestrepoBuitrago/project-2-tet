import os
from flask import Flask
from extensions import db, ma
from controllers.auth_controller import auth
from config import config

def create_app(config_name='default'):
    """Crea y configura la aplicación Flask"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
        
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    ma.init_app(app)
    
    # Registrar blueprints
    app.register_blueprint(auth, url_prefix='/api/v1')
    
    # Crear tablas
    with app.app_context():
        db.create_all()
    
    return app

# Ejecución principal
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5002)