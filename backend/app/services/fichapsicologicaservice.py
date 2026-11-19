from app.core.exceptions import ConflictError
from app.models.fichapsicologica import FichaPsicologica
from app.repositories.estudianterepository import EstudianteRepository
from app.repositories.fichapsicologicarepository import FichaPsicologicaRepository
from app.repositories.personalrepository import PersonalRepository
from app.schemas.fichapsicologica import FichaCreate, FichaRead
from app.services.helpers import asignarcampos, obteneroerror


class FichaPsicologicaService:
    def __init__(
        self,
        fichas: FichaPsicologicaRepository,
        estudiantes: EstudianteRepository,
        personal: PersonalRepository,
    ) -> None:
        self.fichas = fichas
        self.estudiantes = estudiantes
        self.personal = personal

    def listar(self, codest: int | None = None) -> list[FichaRead]:
        fichas = self.fichas.listall() if codest is None else self.fichas.listbyestudiante(codest)
        return [FichaRead.model_validate(ficha) for ficha in fichas]

    def obtener(self, codfic: int) -> FichaRead:
        return FichaRead.model_validate(self.buscar(codfic))

    def crear(self, datos: FichaCreate) -> FichaRead:
        self.validar(datos)
        return FichaRead.model_validate(self.fichas.add(FichaPsicologica(**datos.model_dump())))

    def actualizar(self, codfic: int, datos: FichaCreate) -> FichaRead:
        ficha = self.buscar(codfic)
        self.validar(datos)
        asignarcampos(ficha, datos)
        return FichaRead.model_validate(self.fichas.update(ficha))

    def eliminar(self, codfic: int) -> None:
        self.fichas.delete(self.buscar(codfic))

    def buscar(self, codfic: int) -> FichaPsicologica:
        return obteneroerror(self.fichas, codfic, "La ficha psicológica")

    def validar(self, datos: FichaCreate) -> None:
        obteneroerror(self.estudiantes, datos.codest, "El estudiante")
        obteneroerror(self.personal, datos.codperresp, "El responsable")
        if datos.estfic == "CERRADA" and not (datos.diagfic and datos.planfic):
            raise ConflictError("Para cerrar la ficha hay que completar el diagnóstico y el plan")
