from abc import abstractmethod

from sqlalchemy import select

from app.models.personal import Servicio
from app.repositories.base import BaseRepository, SQLAlchemyRepository


class ServicioRepository(BaseRepository[Servicio]):
    @abstractmethod
    def getbynombre(self, nomserv: str) -> Servicio | None: ...


class SQLAlchemyServicioRepository(SQLAlchemyRepository[Servicio], ServicioRepository):
    model = Servicio

    def getbynombre(self, nomserv: str) -> Servicio | None:
        return self.first(select(Servicio).where(Servicio.nomserv == nomserv))

    def ordering(self):
        return (Servicio.nomserv,)
