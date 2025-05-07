import os

class Config:
    """Configuración base de la aplicación"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SQLALCHEMY_DATABASE_URI_WRITE = os.getenv('WRITE_ENGINE')
    SQLALCHEMY_DATABASE_URI_READ = os.getenv('READER_ENGINE')
    
    if not SQLALCHEMY_DATABASE_URI_READ:
        SQLALCHEMY_DATABASE_URI_READ = SQLALCHEMY_DATABASE_URI_WRITE
    
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI_WRITE

class DevelopmentConfig(Config):
    """Configuración para entorno de desarrollo"""
    DEBUG = True
    
    if not Config.SQLALCHEMY_DATABASE_URI_WRITE:
        SQLALCHEMY_DATABASE_URI_WRITE = 'sqlite:///bookstore.db'
        SQLALCHEMY_DATABASE_URI_READ = 'sqlite:///bookstore.db'
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI_WRITE

class ProductionConfig(Config):
    """Configuración para entorno de producción"""
    DEBUG = False
    
    @classmethod
    def init_app(cls, app):
        assert cls.SQLALCHEMY_DATABASE_URI_WRITE, "No se ha definido WRITE_ENGINE"
        assert cls.AUTH_SERVICE_URL, "No se ha definido AUTH_SERVICE_URL"
        
        if not cls.SQLALCHEMY_DATABASE_URI_READ:
            app.logger.warning("No se ha definido READER_ENGINE, usando WRITE_ENGINE para ambos")

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}