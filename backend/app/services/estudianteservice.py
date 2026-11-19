from app.core.exceptions import ConflictError
from app.models import Estudiante
from app.repositories.escuelarepository import EscuelaRepository
from app.repositories.estudianterepository import EstudianteRepository
from app.schemas.estudiante import EstudianteCreate
from app.services.helpers import asignarcampos, esotroregistro, obteneroerror


class EstudianteService:
    def __init__(self, estudiantes: EstudianteRepository, escuelas: EscuelaRepository) -> None:
        self.estudiantes = estudiantes
        self.escuelas = escuelas

    def listar(self, codesc: int | None = None) -> list[Estudiante]:
        if codesc is None:
            return self.estudiantes.listall()
        return self.estudiantes.listbyescuela(codesc)

    def obtener(self, codest: int) -> Estudiante:
        return obteneroerror(self.estudiantes, codest, "El estudiante")

    def crear(self, datos: EstudianteCreate) -> Estudiante:
        self.validar(datos)
        return self.estudiantes.add(Estudiante(**datos.model_dump()))

    def actualizar(self, codest: int, datos: EstudianteCreate) -> Estudiante:
        estudiante = self.obtener(codest)
        self.validar(datos, codest)
        asignarcampos(estudiante, datos)
        return self.estudiantes.update(estudiante)

    def eliminar(self, codest: int) -> None:
        self.estudiantes.delete(self.obtener(codest))

    def validar(self, datos: EstudianteCreate, codest: int | None = None) -> None:
        obteneroerror(self.escuelas, datos.codesc, "La escuela")
        self.validardniunico(datos.dniest, codest)
        self.validarcorreounico(datos.correst, codest)

    def validardniunico(self, dniest: str, codest: int | None) -> None:
        if esotroregistro(self.estudiantes.getbydni(dniest), "codest", codest):
            raise ConflictError(f"Ya existe un estudiante con DNI {dniest}")

    def validarcorreounico(self, correst: str, codest: int | None) -> None:
        if esotroregistro(self.estudiantes.getbycorreo(correst), "codest", codest):
            raise ConflictError(f"Ya existe un estudiante con el correo {correst}")
