from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import getsettings

engine = create_engine(getsettings().databaseurl, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def getdb() -> Iterator[Session]:
    """Abre una sesión por petición HTTP y la cierra al terminar."""
    with SessionLocal() as session:
        yield session
