import os
from flask import Flask, render_template
from extensions import db
from config import config
from flask import render_template, session
from utils.utils import check_user_auth

def create_app(config_name=None):
    """Crea y configura la aplicación Flask"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
        
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    
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

def initialize_delivery_providers(app):
    from models.delivery import DeliveryProvider
    
    with app.app_context():
        if DeliveryProvider.query.count() == 0:
            session = db.session.using_write_bind()
            providers = [
                DeliveryProvider(name="DHL", coverage_area="Internacional", cost=50.0),
                DeliveryProvider(name="FedEx", coverage_area="Internacional", cost=45.0),
                DeliveryProvider(name="Envia", coverage_area="Nacional", cost=20.0),
                DeliveryProvider(name="Servientrega", coverage_area="Nacional", cost=15.0),
            ]
            session.bulk_save_objects(providers)
            session.commit()

# Ejecución principal
if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        initialize_delivery_providers(app)
    app.run(host="0.0.0.0", debug=True)