from abc import abstractmethod

from sqlalchemy import func, select

from app.models.cita import Atencion
from app.repositories.base import BaseRepository, SQLAlchemyRepository
from app.repositories.procedimientos import llamarmensaje


class AtencionRepository(BaseRepository[Atencion]):
    @abstractmethod
    def findbycita(self, codcita: int) -> Atencion | None: ...

    @abstractmethod
    def registrar(
        self, codcita: int, resumaten: str, recomaten: str | None, nivelaten: str, reqseg: bool
    ) -> str:
        """Registra con el procedimiento p05. Devuelve su mensaje."""

    @abstractmethod
    def nivelriesgo(self, codest: int) -> str:
        """Nivel de vigilancia del estudiante según la función f5."""


class SQLAlchemyAtencionRepository(SQLAlchemyRepository[Atencion], AtencionRepository):
    model = Atencion

    def findbycita(self, codcita: int) -> Atencion | None:
        return self.first(select(Atencion).where(Atencion.codcita == codcita))

    def registrar(
        self, codcita: int, resumaten: str, recomaten: str | None, nivelaten: str, reqseg: bool
    ) -> str:
        return llamarmensaje(
            self.session,
            "call p05(:codcita, :resumen, :recomendacion, :nivel, :reqseg)",
            {
                "codcita": codcita, "resumen": resumaten, "recomendacion": recomaten,
                "nivel": nivelaten, "reqseg": int(reqseg),
            },
        )

    def nivelriesgo(self, codest: int) -> str:
        return self.session.scalar(select(func.f5(codest)))

    def ordering(self):
        return (Atencion.codaten.desc(),)
