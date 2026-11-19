from abc import abstractmethod
from decimal import Decimal

from sqlalchemy import func, select

from app.models.postulacion import Postulacion
from app.repositories.base import BaseRepository, SQLAlchemyRepository
from app.repositories.procedimientos import llamar, llamarmensaje


class PostulacionRepository(BaseRepository[Postulacion]):
    @abstractmethod
    def listfiltered(
        self, codest: int | None, codconv: int | None, estpost: str | None
    ) -> list[Postulacion]: ...

    @abstractmethod
    def findbyestudianteconvocatoria(self, codest: int, codconv: int) -> Postulacion | None: ...

    @abstractmethod
    def registrar(self, codest: int, codconv: int, prompost: Decimal, ingfampost: Decimal) -> str:
        """Registra con el procedimiento p01. Devuelve su mensaje."""

    @abstractmethod
    def evaluar(self, codpost: int, puntpost: Decimal, estpost: str, codpereval: int) -> str:
        """Evalúa con el procedimiento p02. Devuelve su mensaje."""

    @abstractmethod
    def mensajeestado(self, codpost: int) -> str | None:
        """Texto del estado según la función f4."""

    @abstractmethod
    def contarporestudiante(self, codest: int) -> int:
        """Cantidad de postulaciones según la función f1."""


class SQLAlchemyPostulacionRepository(SQLAlchemyRepository[Postulacion], PostulacionRepository):
    model = Postulacion

    def listfiltered(
        self, codest: int | None, codconv: int | None, estpost: str | None
    ) -> list[Postulacion]:
        query = select(Postulacion)
        if codest is not None:
            query = query.where(Postulacion.codest == codest)
        if codconv is not None:
            query = query.where(Postulacion.codconv == codconv)
        if estpost is not None:
            query = query.where(Postulacion.estpost == estpost)
        return self.list(query)

    def findbyestudianteconvocatoria(self, codest: int, codconv: int) -> Postulacion | None:
        return self.first(
            select(Postulacion).where(Postulacion.codest == codest, Postulacion.codconv == codconv)
        )

    def registrar(self, codest: int, codconv: int, prompost: Decimal, ingfampost: Decimal) -> str:
        return llamarmensaje(
            self.session,
            "call p01(:codest, :codconv, :prom, :ingreso)",
            {"codest": codest, "codconv": codconv, "prom": prompost, "ingreso": ingfampost},
        )

    def evaluar(self, codpost: int, puntpost: Decimal, estpost: str, codpereval: int) -> str:
        return llamarmensaje(
            self.session,
            "call p02(:codpost, :punt, :est, :codper)",
            {"codpost": codpost, "punt": puntpost, "est": estpost, "codper": codpereval},
        )

    def mensajeestado(self, codpost: int) -> str | None:
        return self.session.scalar(select(func.f4(codpost)))

    def contarporestudiante(self, codest: int) -> int:
        return self.session.scalar(select(func.f1(codest)))

    def ordering(self):
        return (Postulacion.fechpost.desc(), Postulacion.codpost.desc())
