from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from sqlalchemy.exc import OperationalError, DatabaseError

class RoutingSession(scoped_session):
    def __init__(self, write_session_factory, read_session_factory):
        """
        Inicializa la sesión de enrutamiento con fábricas para escritura y lectura
        """
        self.write_session_factory = write_session_factory
        self.read_session_factory = read_session_factory
        super().__init__(write_session_factory)

    def get_bind(self, mapper=None, clause=None):
        """
        Determina qué base de datos usar en función del tipo de operación
        """
        if self._flushing or self.info.get('writing'):
            return self.write_session_factory.kw['bind']
        else:
            return self.read_session_factory.kw['bind']

    def using_write_bind(self):
        """
        Marca la sesión para usar el endpoint de escritura
        """
        self.info['writing'] = True
        return self
    
    def remove(self):
        """
        Limpia las referencias a la sesión
        """
        self.info.pop('writing', None)
        super().remove()

@retry(
    stop=stop_after_attempt(5),  # Retry 5 times
    wait=wait_exponential(multiplier=1, min=2, max=10),  # Wait 2s, 4s, 8s, 10s, 10s
    retry=retry_if_exception_type((OperationalError, DatabaseError)),  # Retry on connection errors
    reraise=True  # Reraise the last exception if retries fail
)
def create_engine_with_retry(engine_url):
    """
    Crea un motor SQLAlchemy con reintentos y configuración de pool
    """
    return create_engine(
        engine_url,
        pool_size=5,              # Max number of connections in the pool
        max_overflow=10,          # Allow up to 10 additional connections
        pool_timeout=30,          # Wait up to 30s for a connection
        pool_recycle=3600,        # Recycle connections after 1 hour
        pool_pre_ping=True        # Check connection health before use
    )

def create_routing_session(write_engine_url, read_engine_url):
    """
    Crea una sesión que maneja el enrutamiento entre bases de datos de lectura y escritura
    """
    write_engine = create_engine_with_retry(write_engine_url)
    read_engine = create_engine_with_retry(read_engine_url)
    
    write_session_factory = sessionmaker(bind=write_engine)
    read_session_factory = sessionmaker(bind=read_engine)
    
    return RoutingSession(write_session_factory, read_session_factory)