from app.core.exceptions import ConflictError
from app.models.cita import Cita
from app.repositories.citarepository import CitaRepository
from app.repositories.estudianterepository import EstudianteRepository
from app.repositories.personalrepository import PersonalRepository
from app.schemas.cita import CitaCreate, CitaEstado, CitaRead
from app.services.helpers import obteneroerror
from app.services.procedimientos import exigirmensaje

MENSAJECITA = "Cita registrada"


class CitaService:
    def __init__(
        self,
        citas: CitaRepository,
        estudiantes: EstudianteRepository,
        personal: PersonalRepository,
    ) -> None:
        self.citas = citas
        self.estudiantes = estudiantes
        self.personal = personal

    def listar(
        self, codest: int | None = None, codper: int | None = None, estcita: str | None = None
    ) -> list[CitaRead]:
        return [CitaRead.model_validate(cita) for cita in self.citas.listfiltered(codest, codper, estcita)]

    def obtener(self, codcita: int) -> CitaRead:
        return CitaRead.model_validate(self.buscar(codcita))

    def registrar(self, datos: CitaCreate) -> CitaRead:
        obteneroerror(self.estudiantes, datos.codest, "El estudiante")
        obteneroerror(self.personal, datos.codper, "El profesional")
        mensaje = self.citas.registrar(
            datos.codest, datos.codper, datos.fechcita, datos.horacita, datos.modcita, datos.motcita
        )
        exigirmensaje(mensaje, MENSAJECITA)
        creada = self.citas.findbyhorario(datos.codper, datos.fechcita, datos.horacita)
        return CitaRead.model_validate(creada)

    def cambiarestado(self, codcita: int, datos: CitaEstado) -> CitaRead:
        cita = self.buscar(codcita)
        if cita.estcita != "PROGRAMADA":
            raise ConflictError("Solo se puede cambiar el estado de una cita programada")
        cita.estcita = datos.estcita
        return CitaRead.model_validate(self.citas.update(cita))

    def eliminar(self, codcita: int) -> None:
        cita = self.buscar(codcita)
        if cita.atencion is not None:
            raise ConflictError("No se puede eliminar una cita que ya tiene una atención registrada")
        self.citas.delete(cita)

    def buscar(self, codcita: int) -> Cita:
        return obteneroerror(self.citas, codcita, "La cita")
