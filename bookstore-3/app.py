import os
from flask import Flask, render_template, session
from config import config
from utils.utils import check_user_auth

def create_app(config_name=None):
    """Crea y configura la aplicación Flask"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
        
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Registrar Blueprints
    from controllers.auth_controller import auth
    from controllers.book_controller import book
    from controllers.purchase_controller import purchase
    from controllers.payment_controller import payment
    from controllers.delivery_controller import delivery
    from controllers.admin_controller import admin
    
    app.register_blueprint(auth)
    app.register_blueprint(book, url_prefix='/book')
    app.register_blueprint(purchase)
    app.register_blueprint(payment)
    app.register_blueprint(delivery)
    app.register_blueprint(admin)
    
    # Ruta principal
    @app.route('/')
    def home():
        user = check_user_auth(session.get('token'))
        return render_template('home.html', my_user=user)
    
    return app

# Ejecución principal
if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", debug=True)