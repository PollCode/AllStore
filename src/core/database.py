from sqlmodel import create_engine, Session, SQLModel
from .config import settings

    
# Crear el motor de base de datos
engine = create_engine(settings.DATABASE_URL)


def init_db():
    # ⚠️ ELIMINA TODOS LOS DATOS EXISTENTES
    # SQLModel.metadata.drop_all(engine)  
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()