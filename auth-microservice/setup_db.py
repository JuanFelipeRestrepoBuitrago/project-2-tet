from app import app
from extensions import db
from models.user import User
from models.book import Book
from models.delivery import DeliveryProvider
from models.purchase import Purchase
from models.payment import Payment
from models.delivery_assignment import DeliveryAssignment
from sqlalchemy import create_engine, text
import os

def setup_database():
    root_engine = create_engine(os.getenv('CREATION_DB'))
    
    with root_engine.connect() as connection:
        connection.execute(text("CREATE DATABASE IF NOT EXISTS bookstore CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
        connection.commit()

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('WRITE_ENGINE')
    
    with app.app_context():
        db.create_all()
        print("¡Base de datos y tablas creadas exitosamente!")

if __name__ == '__main__':
    setup_database()