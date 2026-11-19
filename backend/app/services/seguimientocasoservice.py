from app.core.exceptions import ConflictError
from app.models.cita import SeguimientoCaso
from app.repositories.atencionrepository import AtencionRepository
from app.repositories.seguimientocasorepository import SeguimientoCasoRepository
from app.schemas.seguimientocaso import (
    SeguimientoCasoCreate,
    SeguimientoCasoRead,
    SeguimientoCasoUpdate,
)
from app.services.helpers import asignarcampos, obteneroerror


class SeguimientoCasoService:
    def __init__(self, seguimientos: SeguimientoCasoRepository, atenciones: AtencionRepository) -> None:
        self.seguimientos = seguimientos
        self.atenciones = atenciones

    def listar(self, codaten: int) -> list[SeguimientoCasoRead]:
        obteneroerror(self.atenciones, codaten, "La atención")
        return [SeguimientoCasoRead.model_validate(item) for item in self.seguimientos.listbyatencion(codaten)]

    def crear(self, datos: SeguimientoCasoCreate) -> SeguimientoCasoRead:
        atencion = obteneroerror(self.atenciones, datos.codaten, "La atención")
        if not atencion.reqseg:
            raise ConflictError("La atención no requiere seguimiento")
        seguimiento = self.seguimientos.add(SeguimientoCaso(**datos.model_dump()))
        return SeguimientoCasoRead.model_validate(seguimiento)

    def actualizar(self, codseg: int, datos: SeguimientoCasoUpdate) -> SeguimientoCasoRead:
        seguimiento = self.buscar(codseg)
        asignarcampos(seguimiento, datos)
        return SeguimientoCasoRead.model_validate(self.seguimientos.update(seguimiento))

    def eliminar(self, codseg: int) -> None:
        self.seguimientos.delete(self.buscar(codseg))

    def buscar(self, codseg: int) -> SeguimientoCaso:
        return obteneroerror(self.seguimientos, codseg, "El seguimiento")
