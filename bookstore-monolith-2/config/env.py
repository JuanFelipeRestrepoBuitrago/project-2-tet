import os

SQLALCHEMY_DATABASE_URI = os.getenv(
    'DATABASE_URL',
    'mysql+pymysql://bookstore_user:123@localhost/bookstore'
)
SECRET_KEY = os.getenv('SECRET_KEY', 'secretkey')
SQLALCHEMY_TRACK_MODIFICATIONS = bool(os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False))
