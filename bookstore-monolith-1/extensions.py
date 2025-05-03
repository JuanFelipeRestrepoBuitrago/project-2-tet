from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Extensiones globales para usar en toda la app
db = SQLAlchemy()
login_manager = LoginManager()
