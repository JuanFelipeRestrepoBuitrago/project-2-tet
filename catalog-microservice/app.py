from flask import Flask, render_template
from extensions import db
from config import config
import os

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)

    from controllers.book_controller import book
    app.register_blueprint(book, url_prefix='/book')

    @app.route('/')
    def home():
        return render_template('catalog.html')

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5002, debug=True)