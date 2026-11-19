from app.core.exceptions import ConflictError
from app.models import Requisito
from app.repositories.requisitorepository import RequisitoRepository
from app.schemas.requisito import RequisitoCreate
from app.services.helpers import asignarcampos, esotroregistro, obteneroerror


class RequisitoService:
    def __init__(self, requisitos: RequisitoRepository) -> None:
        self.requisitos = requisitos

    def listar(self) -> list[Requisito]:
        return self.requisitos.listall()

    def obtener(self, codreq: int) -> Requisito:
        return obteneroerror(self.requisitos, codreq, "El requisito")

    def crear(self, datos: RequisitoCreate) -> Requisito:
        self.validarnombreunico(datos.nomreq)
        return self.requisitos.add(Requisito(**datos.model_dump()))

    def actualizar(self, codreq: int, datos: RequisitoCreate) -> Requisito:
        requisito = self.obtener(codreq)
        self.validarnombreunico(datos.nomreq, codreq)
        asignarcampos(requisito, datos)
        return self.requisitos.update(requisito)

    def eliminar(self, codreq: int) -> None:
        requisito = self.obtener(codreq)
        if self.requisitos.isassignedtobeca(codreq):
            raise ConflictError("No se puede eliminar un requisito asignado a una beca")
        self.requisitos.delete(requisito)

    def validarnombreunico(self, nomreq: str, codreq: int | None = None) -> None:
        if esotroregistro(self.requisitos.getbynombre(nomreq), "codreq", codreq):
            raise ConflictError(f"Ya existe el requisito '{nomreq}'")
