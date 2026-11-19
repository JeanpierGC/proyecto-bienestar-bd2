from app.core.exceptions import ConflictError
from app.models import Convocatoria
from app.repositories.becarepository import BecaRepository
from app.repositories.convocatoriarepository import ConvocatoriaRepository
from app.schemas.convocatoria import ConvocatoriaCreate, ConvocatoriaRead
from app.services.helpers import asignarcampos, obteneroerror


class ConvocatoriaService:
    def __init__(self, convocatorias: ConvocatoriaRepository, becas: BecaRepository) -> None:
        self.convocatorias = convocatorias
        self.becas = becas

    def listar(self, codbeca: int | None = None) -> list[ConvocatoriaRead]:
        if codbeca is None:
            convocatorias = self.convocatorias.listall()
        else:
            convocatorias = self.convocatorias.listbybeca(codbeca)
        return [self.concupos(convocatoria) for convocatoria in convocatorias]

    def obtener(self, codconv: int) -> ConvocatoriaRead:
        return self.concupos(self.buscar(codconv))

    def crear(self, datos: ConvocatoriaCreate) -> ConvocatoriaRead:
        self.validarbecaactiva(datos.codbeca)
        convocatoria = self.convocatorias.add(Convocatoria(**datos.model_dump()))
        return self.concupos(convocatoria)

    def actualizar(self, codconv: int, datos: ConvocatoriaCreate) -> ConvocatoriaRead:
        convocatoria = self.buscar(codconv)
        self.validarbecaactiva(datos.codbeca)
        asignarcampos(convocatoria, datos)
        return self.concupos(self.convocatorias.update(convocatoria))

    def eliminar(self, codconv: int) -> None:
        self.convocatorias.delete(self.buscar(codconv))

    def buscar(self, codconv: int) -> Convocatoria:
        return obteneroerror(self.convocatorias, codconv, "La convocatoria")

    def validarbecaactiva(self, codbeca: int) -> None:
        beca = obteneroerror(self.becas, codbeca, "La beca")
        if beca.estbeca != "ACTIVA":
            raise ConflictError("No se puede usar una beca inactiva en una convocatoria")

    def concupos(self, convocatoria: Convocatoria) -> ConvocatoriaRead:
        lectura = ConvocatoriaRead.model_validate(convocatoria)
        lectura.cuposdisponibles = self.convocatorias.cuposdisponibles(convocatoria.codconv)
        return lectura
