from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import create_engine
import os

# Configuración básica
db = SQLAlchemy()
login_manager = LoginManager()

# Configuración de engines
write_engine_string = os.getenv('WRITE_ENGINE')
reader_engine_string = os.getenv('READER_ENGINE')

# Solo creamos los engines, Flask-SQLAlchemy manejará las sesiones
writer_engine = create_engine(write_engine_string)
reader_engine = create_engine(reader_engine_string)