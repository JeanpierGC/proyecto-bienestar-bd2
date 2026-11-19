from app.core.exceptions import ConflictError
from app.models import Facultad
from app.repositories.escuelarepository import EscuelaRepository
from app.repositories.facultadrepository import FacultadRepository
from app.schemas.facultad import FacultadCreate
from app.services.helpers import asignarcampos, esotroregistro, obteneroerror


class FacultadService:
    def __init__(self, facultades: FacultadRepository, escuelas: EscuelaRepository) -> None:
        self.facultades = facultades
        self.escuelas = escuelas

    def listar(self) -> list[Facultad]:
        return self.facultades.listall()

    def obtener(self, codfac: int) -> Facultad:
        return obteneroerror(self.facultades, codfac, "La facultad")

    def crear(self, datos: FacultadCreate) -> Facultad:
        self.validarnombreunico(datos.nomfac)
        return self.facultades.add(Facultad(**datos.model_dump()))

    def actualizar(self, codfac: int, datos: FacultadCreate) -> Facultad:
        facultad = self.obtener(codfac)
        self.validarnombreunico(datos.nomfac, codfac)
        asignarcampos(facultad, datos)
        return self.facultades.update(facultad)

    def eliminar(self, codfac: int) -> None:
        facultad = self.obtener(codfac)
        if self.escuelas.existsbyfacultad(codfac):
            raise ConflictError("No se puede eliminar una facultad que tiene escuelas")
        self.facultades.delete(facultad)

    def validarnombreunico(self, nomfac: str, codfac: int | None = None) -> None:
        existente = self.facultades.getbynombre(nomfac)
        if esotroregistro(existente, "codfac", codfac):
            raise ConflictError(f"Ya existe la facultad '{nomfac}'")
