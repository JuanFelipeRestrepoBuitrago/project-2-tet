import os

SECRET_KEY = os.getenv('SECRET_KEY', 'secretkey')
SQLALCHEMY_TRACK_MODIFICATIONS = bool(os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False))
