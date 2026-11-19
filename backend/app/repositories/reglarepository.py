from abc import abstractmethod

from sqlalchemy import select

from app.models import Regla
from app.repositories.base import BaseRepository, SQLAlchemyRepository


class ReglaRepository(BaseRepository[Regla]):
    @abstractmethod
    def listbybeca(self, codbeca: int) -> list[Regla]: ...


class SQLAlchemyReglaRepository(SQLAlchemyRepository[Regla], ReglaRepository):
    model = Regla

    def listbybeca(self, codbeca: int) -> list[Regla]:
        return self.list(select(Regla).where(Regla.codbeca == codbeca))

    def ordering(self):
        return (Regla.codbeca, Regla.codreg)
