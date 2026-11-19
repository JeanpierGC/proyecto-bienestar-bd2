from app.core.exceptions import ConflictError, NotFoundError
from app.models import Beca
from app.repositories.becarepository import BecaRepository
from app.repositories.convocatoriarepository import ConvocatoriaRepository
from app.repositories.requisitorepository import RequisitoRepository
from app.schemas.beca import BecaCreate, BecaRequisitosUpdate
from app.services.helpers import asignarcampos, esotroregistro, obteneroerror


class BecaService:
    def __init__(
        self,
        becas: BecaRepository,
        convocatorias: ConvocatoriaRepository,
        requisitos: RequisitoRepository,
    ) -> None:
        self.becas = becas
        self.convocatorias = convocatorias
        self.requisitos = requisitos

    def listar(self) -> list[Beca]:
        return self.becas.listall()

    def obtener(self, codbeca: int) -> Beca:
        return obteneroerror(self.becas, codbeca, "La beca")

    def crear(self, datos: BecaCreate) -> Beca:
        self.validarnombreunico(datos.nombeca)
        return self.becas.add(Beca(**datos.model_dump()))

    def actualizar(self, codbeca: int, datos: BecaCreate) -> Beca:
        beca = self.obtener(codbeca)
        self.validarnombreunico(datos.nombeca, codbeca)
        asignarcampos(beca, datos)
        return self.becas.update(beca)

    def eliminar(self, codbeca: int) -> None:
        beca = self.obtener(codbeca)
        if self.convocatorias.existsbybeca(codbeca):
            raise ConflictError("No se puede eliminar una beca que tiene convocatorias")
        self.becas.delete(beca)

    def asignarrequisitos(self, codbeca: int, datos: BecaRequisitosUpdate) -> Beca:
        beca = self.obtener(codbeca)
        codigos = sorted(set(datos.codreq))
        requisitos = self.requisitos.listbyids(codigos) if codigos else []
        faltantes = set(codigos) - {requisito.codreq for requisito in requisitos}
        if faltantes:
            raise NotFoundError(f"Los requisitos {sorted(faltantes)} no existen")
        beca.requisitos = requisitos
        return self.becas.update(beca)

    def validarnombreunico(self, nombeca: str, codbeca: int | None = None) -> None:
        if esotroregistro(self.becas.getbynombre(nombeca), "codbeca", codbeca):
            raise ConflictError(f"Ya existe la beca '{nombeca}'")
