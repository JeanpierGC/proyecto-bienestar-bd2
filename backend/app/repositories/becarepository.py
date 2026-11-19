from abc import abstractmethod

from sqlalchemy import select

from app.models import Beca
from app.repositories.base import BaseRepository, SQLAlchemyRepository


class BecaRepository(BaseRepository[Beca]):
    @abstractmethod
    def getbynombre(self, nombeca: str) -> Beca | None: ...


class SQLAlchemyBecaRepository(SQLAlchemyRepository[Beca], BecaRepository):
    model = Beca

    def getbynombre(self, nombeca: str) -> Beca | None:
        return self.first(select(Beca).where(Beca.nombeca == nombeca))

    def ordering(self):
        return (Beca.nombeca,)
