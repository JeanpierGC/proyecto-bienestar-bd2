from app.core.exceptions import ConflictError
from app.models import Escuela
from app.repositories.escuelarepository import EscuelaRepository
from app.repositories.estudianterepository import EstudianteRepository
from app.repositories.facultadrepository import FacultadRepository
from app.schemas.escuela import EscuelaCreate
from app.services.helpers import asignarcampos, esotroregistro, obteneroerror


class EscuelaService:
    def __init__(
        self,
        escuelas: EscuelaRepository,
        facultades: FacultadRepository,
        estudiantes: EstudianteRepository,
    ) -> None:
        self.escuelas = escuelas
        self.facultades = facultades
        self.estudiantes = estudiantes

    def listar(self, codfac: int | None = None) -> list[Escuela]:
        if codfac is None:
            return self.escuelas.listall()
        return self.escuelas.listbyfacultad(codfac)

    def obtener(self, codesc: int) -> Escuela:
        return obteneroerror(self.escuelas, codesc, "La escuela")

    def crear(self, datos: EscuelaCreate) -> Escuela:
        self.validar(datos)
        return self.escuelas.add(Escuela(**datos.model_dump()))

    def actualizar(self, codesc: int, datos: EscuelaCreate) -> Escuela:
        escuela = self.obtener(codesc)
        self.validar(datos, codesc)
        asignarcampos(escuela, datos)
        return self.escuelas.update(escuela)

    def eliminar(self, codesc: int) -> None:
        escuela = self.obtener(codesc)
        if self.estudiantes.existsbyescuela(codesc):
            raise ConflictError("No se puede eliminar una escuela que tiene estudiantes")
        self.escuelas.delete(escuela)

    def validar(self, datos: EscuelaCreate, codesc: int | None = None) -> None:
        obteneroerror(self.facultades, datos.codfac, "La facultad")
        existente = self.escuelas.getbynombre(datos.nomesc, datos.codfac)
        if esotroregistro(existente, "codesc", codesc):
            raise ConflictError(f"La escuela '{datos.nomesc}' ya existe en esa facultad")
