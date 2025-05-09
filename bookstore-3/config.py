import os

class Config:
    """Configuración base de la aplicación"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'secretkey')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    AUTH_SERVICE_URL = os.getenv('AUTH_SERVICE_URL')
    CATALOG_SERVICE_URL = os.getenv('CATALOG_SERVICE_URL')
    PURCHASE_SERVICE_URL = os.getenv('PURCHASE_SERVICE_URL')

class DevelopmentConfig(Config):
    """Configuración para entorno de desarrollo"""
    DEBUG = True

class ProductionConfig(Config):
    """Configuración para entorno de producción"""
    DEBUG = False
    
    @classmethod
    def init_app(cls, app):
        assert cls.AUTH_SERVICE_URL, "No se ha definido AUTH_SERVICE_URL"
        assert cls.CATALOG_SERVICE_URL, "No se ha definido CATALOG_SERVICE_URL"
        assert cls.PURCHASE_SERVICE_URL, "No se ha definido PURCHASE_SERVICE_URL"

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}