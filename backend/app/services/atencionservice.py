from app.core.exceptions import NotFoundError
from app.models.cita import Atencion
from app.repositories.atencionrepository import AtencionRepository
from app.schemas.atencion import AtencionCreate, AtencionRead, RiesgoEstudiante
from app.services.helpers import obteneroerror
from app.services.procedimientos import exigirmensaje

MENSAJEATENCION = "Atención registrada"
MENSAJESINESTUDIANTE = "Estudiante no existe"


class AtencionService:
    def __init__(self, atenciones: AtencionRepository) -> None:
        self.atenciones = atenciones

    def listar(self, codest: int | None = None) -> list[AtencionRead]:
        return [
            self.lectura(atencion)
            for atencion in self.atenciones.listall()
            if codest is None or atencion.cita.codest == codest
        ]

    def obtener(self, codaten: int) -> AtencionRead:
        return self.lectura(self.buscar(codaten))

    def registrar(self, datos: AtencionCreate) -> AtencionRead:
        mensaje = self.atenciones.registrar(
            datos.codcita, datos.resumaten, datos.recomaten, datos.nivelaten, datos.reqseg
        )
        exigirmensaje(mensaje, MENSAJEATENCION)
        return self.lectura(self.atenciones.findbycita(datos.codcita))

    def riesgo(self, codest: int) -> RiesgoEstudiante:
        nivel = self.atenciones.nivelriesgo(codest)
        if nivel == MENSAJESINESTUDIANTE:
            raise NotFoundError(f"El estudiante con código {codest} no existe")
        return RiesgoEstudiante(codest=codest, nivel=nivel)

    def buscar(self, codaten: int) -> Atencion:
        return obteneroerror(self.atenciones, codaten, "La atención")

    def lectura(self, atencion: Atencion) -> AtencionRead:
        lectura = AtencionRead.model_validate(atencion)
        lectura.cantseguimientos = len(atencion.seguimientos)
        return lectura
