from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_login import LoginManager
from sqlalchemy.orm import sessionmaker, scoped_session
import os

# Extensiones globales para usar en toda la app
db = SQLAlchemy()
login_manager = LoginManager()

write_engine_string = os.getenv('WRITE_ENGINE')
reader_engine_string = os.getenv('READER_ENGINE')

writer_engine = create_engine(write_engine_string)
reader_engine = create_engine(reader_engine_string)

class RoutingSession(scoped_session):
    def get_bind(self, mapper=None, clause=None):
        if self._flushing or (mapper and mapper.persist_only):
            return writer_engine
        return reader_engine

db.session = RoutingSession(sessionmaker(autocommit=False, autoflush=False, bind=writer_engine))