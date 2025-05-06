import os
from flask import Flask, render_template
from extensions import db, login_manager
from controllers.auth_controller import auth
from models.user import User
from config import config

def create_app(config_name=None):
    """Crea y configura la aplicación Flask"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
        
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    app.register_blueprint(auth)
    
    return app

# Ejecución principal
if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", debug=True)