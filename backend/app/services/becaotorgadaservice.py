from app.core.exceptions import ConflictError
from app.models.becaotorgada import BecaOtorgada, SeguimientoBeca
from app.repositories.becaotorgadarepository import (
    BecaOtorgadaRepository,
    SeguimientoBecaRepository,
)
from app.repositories.personalrepository import PersonalRepository
from app.schemas.becaotorgada import (
    BecaOtorgadaCreate,
    BecaOtorgadaEstado,
    BecaOtorgadaRead,
    SeguimientoBecaCreate,
    SeguimientoBecaRead,
)
from app.services.helpers import obteneroerror
from app.services.procedimientos import exigirmensaje

MENSAJEOTORGADA = "Beca otorgada"


class BecaOtorgadaService:
    def __init__(
        self,
        otorgadas: BecaOtorgadaRepository,
        seguimientos: SeguimientoBecaRepository,
        personal: PersonalRepository,
    ) -> None:
        self.otorgadas = otorgadas
        self.seguimientos = seguimientos
        self.personal = personal

    def listar(self, codest: int | None = None) -> list[BecaOtorgadaRead]:
        return [
            self.conpromedio(otorgada)
            for otorgada in self.otorgadas.listall()
            if codest is None or otorgada.postulacion.codest == codest
        ]

    def obtener(self, codotor: int) -> BecaOtorgadaRead:
        return self.conpromedio(self.buscar(codotor))

    def otorgar(self, datos: BecaOtorgadaCreate) -> BecaOtorgadaRead:
        mensaje = self.otorgadas.otorgar(datos.codpost, datos.fechiniotor, datos.fechfinotor)
        exigirmensaje(mensaje, MENSAJEOTORGADA)
        return self.conpromedio(self.otorgadas.findbypostulacion(datos.codpost))

    def cambiarestado(self, codotor: int, datos: BecaOtorgadaEstado) -> BecaOtorgadaRead:
        otorgada = self.buscar(codotor)
        otorgada.estotor = datos.estotor
        return self.conpromedio(self.otorgadas.update(otorgada))

    def eliminar(self, codotor: int) -> None:
        otorgada = self.buscar(codotor)
        if otorgada.seguimientos:
            raise ConflictError("No se puede eliminar una beca otorgada que tiene seguimientos")
        self.otorgadas.delete(otorgada)

    def listarseguimientos(self, codotor: int) -> list[SeguimientoBecaRead]:
        self.buscar(codotor)
        return [SeguimientoBecaRead.model_validate(item)
                for item in self.seguimientos.listbyotorgada(codotor)]

    def registrarseguimiento(
        self, codotor: int, datos: SeguimientoBecaCreate
    ) -> SeguimientoBecaRead:
        self.buscar(codotor)
        obteneroerror(self.personal, datos.codperresp, "El responsable")
        seguimiento = self.seguimientos.add(SeguimientoBeca(codotor=codotor, **datos.model_dump()))
        return SeguimientoBecaRead.model_validate(seguimiento)

    def eliminarseguimiento(self, codotor: int, codsegb: int) -> None:
        self.buscar(codotor)
        seguimiento = obteneroerror(self.seguimientos, codsegb, "El seguimiento")
        if seguimiento.codotor != codotor:
            raise ConflictError("El seguimiento no pertenece a esta beca otorgada")
        self.seguimientos.delete(seguimiento)

    def buscar(self, codotor: int) -> BecaOtorgada:
        return obteneroerror(self.otorgadas, codotor, "La beca otorgada")

    def conpromedio(self, otorgada: BecaOtorgada) -> BecaOtorgadaRead:
        lectura = BecaOtorgadaRead.model_validate(otorgada)
        lectura.cantseguimientos = len(otorgada.seguimientos)
        promedio = self.otorgadas.promedioseguimiento(otorgada.codotor)
        lectura.promedioseguimiento = float(promedio) if promedio is not None else None
        return lectura
