from abc import abstractmethod

from sqlalchemy import exists, select

from app.models import Requisito
from app.models.requisito import requisitobeca
from app.repositories.base import BaseRepository, SQLAlchemyRepository


class RequisitoRepository(BaseRepository[Requisito]):
    @abstractmethod
    def getbynombre(self, nomreq: str) -> Requisito | None: ...

    @abstractmethod
    def listbyids(self, codigos: list[int]) -> list[Requisito]: ...

    @abstractmethod
    def isassignedtobeca(self, codreq: int) -> bool: ...


class SQLAlchemyRequisitoRepository(SQLAlchemyRepository[Requisito], RequisitoRepository):
    model = Requisito

    def getbynombre(self, nomreq: str) -> Requisito | None:
        return self.first(select(Requisito).where(Requisito.nomreq == nomreq))

    def listbyids(self, codigos: list[int]) -> list[Requisito]:
        return self.list(select(Requisito).where(Requisito.codreq.in_(codigos)))

    def isassignedtobeca(self, codreq: int) -> bool:
        return self.session.scalar(select(exists().where(requisitobeca.c.codreq == codreq)))

    def ordering(self):
        return (Requisito.nomreq,)
