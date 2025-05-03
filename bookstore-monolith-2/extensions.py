import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import sessionmaker
from bindings import create_routing_session

class RoutingSQLAlchemy(SQLAlchemy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.write_engine_url = None
        self.read_engine_url = None

    def init_app(self, app):
        """Inicializa la aplicación con soporte para enrutamiento de DB"""
        super().init_app(app)
        
        self.write_engine_url = app.config['SQLALCHEMY_DATABASE_URI_WRITE']
        self.read_engine_url = app.config['SQLALCHEMY_DATABASE_URI_READ']
        
        if not self.read_engine_url:
            self.read_engine_url = self.write_engine_url
            
        session = create_routing_session(self.write_engine_url, self.read_engine_url)
        
        self.session = session

db = RoutingSQLAlchemy()
login_manager = LoginManager()