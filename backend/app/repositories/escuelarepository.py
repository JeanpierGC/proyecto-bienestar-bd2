from abc import abstractmethod

from sqlalchemy import exists, func, select

from app.models import Escuela, Estudiante, Facultad
from app.repositories.base import BaseRepository, SQLAlchemyRepository


class EscuelaRepository(BaseRepository[Escuela]):
    @abstractmethod
    def getbynombre(self, nomesc: str, codfac: int) -> Escuela | None: ...

    @abstractmethod
    def listbyfacultad(self, codfac: int) -> list[Escuela]: ...

    @abstractmethod
    def existsbyfacultad(self, codfac: int) -> bool: ...

    @abstractmethod
    def countestudiantes(self) -> list[tuple[int, str, str, int]]:
        """(codesc, nomesc, nomfac, total de estudiantes), de mayor a menor."""


class SQLAlchemyEscuelaRepository(SQLAlchemyRepository[Escuela], EscuelaRepository):
    model = Escuela

    def getbynombre(self, nomesc: str, codfac: int) -> Escuela | None:
        query = select(Escuela).where(Escuela.nomesc == nomesc, Escuela.codfac == codfac)
        return self.first(query)

    def listbyfacultad(self, codfac: int) -> list[Escuela]:
        return self.list(select(Escuela).where(Escuela.codfac == codfac))

    def existsbyfacultad(self, codfac: int) -> bool:
        return self.session.scalar(select(exists().where(Escuela.codfac == codfac)))

    def countestudiantes(self) -> list[tuple[int, str, str, int]]:
        total = func.count(Estudiante.codest)
        query = (
            select(Escuela.codesc, Escuela.nomesc, Facultad.nomfac, total)
            .join(Facultad, Escuela.codfac == Facultad.codfac)
            .outerjoin(Estudiante, Estudiante.codesc == Escuela.codesc)
            .group_by(Escuela.codesc, Escuela.nomesc, Facultad.nomfac)
            .order_by(total.desc(), Escuela.nomesc)
        )
        return [tuple(row) for row in self.session.execute(query)]

    def ordering(self):
        return (Escuela.nomesc,)
