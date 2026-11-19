from abc import abstractmethod

from sqlalchemy import exists, func, select

from app.models import Estudiante
from app.repositories.base import BaseRepository, SQLAlchemyRepository


class EstudianteRepository(BaseRepository[Estudiante]):
    @abstractmethod
    def getbydni(self, dniest: str) -> Estudiante | None: ...

    @abstractmethod
    def getbycorreo(self, correst: str) -> Estudiante | None: ...

    @abstractmethod
    def listbyescuela(self, codesc: int) -> list[Estudiante]: ...

    @abstractmethod
    def existsbyescuela(self, codesc: int) -> bool: ...

    @abstractmethod
    def countbyciclo(self) -> dict[int, int]: ...

    @abstractmethod
    def averageciclo(self) -> float | None: ...

    @abstractmethod
    def listlatest(self, limit: int) -> list[Estudiante]: ...


class SQLAlchemyEstudianteRepository(SQLAlchemyRepository[Estudiante], EstudianteRepository):
    model = Estudiante

    def getbydni(self, dniest: str) -> Estudiante | None:
        return self.first(select(Estudiante).where(Estudiante.dniest == dniest))

    def getbycorreo(self, correst: str) -> Estudiante | None:
        return self.first(select(Estudiante).where(Estudiante.correst == correst))

    def listbyescuela(self, codesc: int) -> list[Estudiante]:
        return self.list(select(Estudiante).where(Estudiante.codesc == codesc))

    def existsbyescuela(self, codesc: int) -> bool:
        return self.session.scalar(select(exists().where(Estudiante.codesc == codesc)))

    def countbyciclo(self) -> dict[int, int]:
        query = select(Estudiante.cicest, func.count()).group_by(Estudiante.cicest)
        return {ciclo: total for ciclo, total in self.session.execute(query)}

    def averageciclo(self) -> float | None:
        promedio = self.session.scalar(select(func.avg(Estudiante.cicest)))
        return None if promedio is None else float(promedio)

    def listlatest(self, limit: int) -> list[Estudiante]:
        query = select(Estudiante).order_by(Estudiante.codest.desc()).limit(limit)
        return list(self.session.scalars(query).unique())

    def ordering(self):
        return (Estudiante.apeest, Estudiante.nomest)
