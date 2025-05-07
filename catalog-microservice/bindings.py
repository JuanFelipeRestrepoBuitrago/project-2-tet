from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

class RoutingSession(scoped_session):
    def __init__(self, write_session_factory, read_session_factory):
        self.write_session_factory = write_session_factory
        self.read_session_factory = read_session_factory
        super().__init__(write_session_factory)

    def get_bind(self, mapper=None, clause=None):
        if self._flushing or self.info.get('writing'):
            return self.write_session_factory.kw['bind']
        else:
            return self.read_session_factory.kw['bind']

    def using_write_bind(self):
        self.info['writing'] = True
        return self

    def remove(self):
        self.info.pop('writing', None)
        super().remove()

def create_routing_session(write_engine_url, read_engine_url):
    write_engine = create_engine(write_engine_url, pool_recycle=3600)
    read_engine = create_engine(read_engine_url, pool_recycle=3600)
    write_session_factory = sessionmaker(bind=write_engine)
    read_session_factory = sessionmaker(bind=read_engine)
    return RoutingSession(write_session_factory, read_session_factory)
