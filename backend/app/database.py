from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from .config import settings

# Crear el motor de base de datos asíncrono
engine = create_async_engine(settings.DATABASE_URL)

# Crear un generador de sesiones asíncronas
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para los modelos de SQLAlchemy
class Base(DeclarativeBase):
    pass

# Dependencia para obtener la sesión de la base de datos en los endpoints
async def get_db():
    async with SessionLocal() as db:
        yield db
