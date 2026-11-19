from abc import abstractmethod

from sqlalchemy import select

from app.models import Facultad
from app.repositories.base import BaseRepository, SQLAlchemyRepository


class FacultadRepository(BaseRepository[Facultad]):
    @abstractmethod
    def getbynombre(self, nomfac: str) -> Facultad | None: ...


class SQLAlchemyFacultadRepository(SQLAlchemyRepository[Facultad], FacultadRepository):
    model = Facultad

    def getbynombre(self, nomfac: str) -> Facultad | None:
        return self.first(select(Facultad).where(Facultad.nomfac == nomfac))

    def ordering(self):
        return (Facultad.nomfac,)
