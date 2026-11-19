from app.models import Regla
from app.repositories.becarepository import BecaRepository
from app.repositories.reglarepository import ReglaRepository
from app.schemas.regla import ReglaCreate
from app.services.helpers import asignarcampos, obteneroerror


class ReglaService:
    def __init__(self, reglas: ReglaRepository, becas: BecaRepository) -> None:
        self.reglas = reglas
        self.becas = becas

    def listar(self, codbeca: int | None = None) -> list[Regla]:
        if codbeca is None:
            return self.reglas.listall()
        return self.reglas.listbybeca(codbeca)

    def obtener(self, codreg: int) -> Regla:
        return obteneroerror(self.reglas, codreg, "La regla")

    def crear(self, datos: ReglaCreate) -> Regla:
        obteneroerror(self.becas, datos.codbeca, "La beca")
        return self.reglas.add(Regla(**datos.model_dump()))

    def actualizar(self, codreg: int, datos: ReglaCreate) -> Regla:
        regla = self.obtener(codreg)
        obteneroerror(self.becas, datos.codbeca, "La beca")
        asignarcampos(regla, datos)
        return self.reglas.update(regla)

    def eliminar(self, codreg: int) -> None:
        self.reglas.delete(self.obtener(codreg))
