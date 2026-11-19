from abc import abstractmethod

from sqlalchemy import exists, func, select

from app.models import Convocatoria
from app.repositories.base import BaseRepository, SQLAlchemyRepository


class ConvocatoriaRepository(BaseRepository[Convocatoria]):
    @abstractmethod
    def listbybeca(self, codbeca: int) -> list[Convocatoria]: ...

    @abstractmethod
    def existsbybeca(self, codbeca: int) -> bool: ...

    @abstractmethod
    def cuposdisponibles(self, codconv: int) -> int | None:
        """Cupos que quedan según la función f6 de la base de datos."""


class SQLAlchemyConvocatoriaRepository(
    SQLAlchemyRepository[Convocatoria], ConvocatoriaRepository
):
    model = Convocatoria

    def listbybeca(self, codbeca: int) -> list[Convocatoria]:
        return self.list(select(Convocatoria).where(Convocatoria.codbeca == codbeca))

    def existsbybeca(self, codbeca: int) -> bool:
        return self.session.scalar(select(exists().where(Convocatoria.codbeca == codbeca)))

    def cuposdisponibles(self, codconv: int) -> int | None:
        return self.session.scalar(select(func.f6(codconv)))

    def ordering(self):
        return (Convocatoria.fechinconv.desc(), Convocatoria.nomconv)
