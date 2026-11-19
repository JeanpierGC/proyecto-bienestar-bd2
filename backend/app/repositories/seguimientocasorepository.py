from abc import abstractmethod

from sqlalchemy import select

from app.models.cita import SeguimientoCaso
from app.repositories.base import BaseRepository, SQLAlchemyRepository


class SeguimientoCasoRepository(BaseRepository[SeguimientoCaso]):
    @abstractmethod
    def listbyatencion(self, codaten: int) -> list[SeguimientoCaso]: ...


class SQLAlchemySeguimientoCasoRepository(
    SQLAlchemyRepository[SeguimientoCaso], SeguimientoCasoRepository
):
    model = SeguimientoCaso

    def listbyatencion(self, codaten: int) -> list[SeguimientoCaso]:
        return self.list(select(SeguimientoCaso).where(SeguimientoCaso.codaten == codaten))

    def ordering(self):
        return (SeguimientoCaso.fechseg.desc(), SeguimientoCaso.codseg.desc())
