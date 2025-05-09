import os
from flask import Flask
from extensions import db
from config import config
from controllers.purchase_controller import purchase
from controllers.payment_controller import payment
from controllers.delivery_controller import delivery
from models.delivery import DeliveryProvider
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from sqlalchemy.exc import OperationalError, DatabaseError

def create_app(config_name=None):
    """Crea y configura la aplicación Flask"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
        
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    
    app.register_blueprint(purchase, url_prefix='/purchase')
    app.register_blueprint(payment, url_prefix='/purchase')
    app.register_blueprint(delivery, url_prefix='/purchase')
    
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
        initialize_delivery_providers(app)

def initialize_delivery_providers(app):    
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
    try:
        initialize_database(app)
    except Exception as e:
        print(f"Failed to initialize database after retries: {e}")
        raise
    app.run(host="0.0.0.0", debug=True)