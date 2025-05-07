from flask import Flask
from extensions import db
from config import config
import os
from controllers.book_controller import book

def create_app(config_name='default'):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(book, url_prefix='/catalog')
    
    return app

if __name__ == '__main__':
    app = create_app()
    # Create database tables
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", debug=True)