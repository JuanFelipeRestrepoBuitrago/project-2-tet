import os

# Configuración principal de la aplicación Flask
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://bookstore_user:bookstore_pass@db/bookstore'
    )
    SECRET_KEY = os.getenv('SECRET_KEY', 'secretkey')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
