import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'secretkey')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI_WRITE = os.getenv('WRITE_ENGINE')
    SQLALCHEMY_DATABASE_URI_READ = os.getenv('READER_ENGINE') or SQLALCHEMY_DATABASE_URI_WRITE
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI_WRITE

class DevelopmentConfig(Config):
    DEBUG = True
    if not Config.SQLALCHEMY_DATABASE_URI_WRITE:
        SQLALCHEMY_DATABASE_URI_WRITE = 'sqlite:///bookstore.db'
        SQLALCHEMY_DATABASE_URI_READ = 'sqlite:///bookstore.db'
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI_WRITE

class ProductionConfig(Config):
    DEBUG = False
    @classmethod
    def init_app(cls, app):
        assert cls.SQLALCHEMY_DATABASE_URI_WRITE, "No se ha definido WRITE_ENGINE"

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
