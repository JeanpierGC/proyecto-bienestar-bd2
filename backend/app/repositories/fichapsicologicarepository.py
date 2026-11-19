from abc import abstractmethod

from sqlalchemy import select

from app.models.fichapsicologica import FichaPsicologica
from app.repositories.base import BaseRepository, SQLAlchemyRepository


class FichaPsicologicaRepository(BaseRepository[FichaPsicologica]):
    @abstractmethod
    def listbyestudiante(self, codest: int) -> list[FichaPsicologica]: ...


class SQLAlchemyFichaPsicologicaRepository(
    SQLAlchemyRepository[FichaPsicologica], FichaPsicologicaRepository
):
    model = FichaPsicologica

    def listbyestudiante(self, codest: int) -> list[FichaPsicologica]:
        return self.list(select(FichaPsicologica).where(FichaPsicologica.codest == codest))

    def ordering(self):
        return (FichaPsicologica.fechaper.desc(), FichaPsicologica.codfic.desc())
