from app.core.exceptions import ConflictError
from app.models.personal import Servicio
from app.repositories.personalrepository import PersonalRepository
from app.repositories.serviciorepository import ServicioRepository
from app.schemas.servicio import ServicioCreate, ServicioRead
from app.services.helpers import asignarcampos, esotroregistro, obteneroerror


class ServicioService:
    def __init__(self, servicios: ServicioRepository, personal: PersonalRepository) -> None:
        self.servicios = servicios
        self.personal = personal

    def listar(self) -> list[ServicioRead]:
        return [ServicioRead.model_validate(servicio) for servicio in self.servicios.listall()]

    def obtener(self, codserv: int) -> ServicioRead:
        return ServicioRead.model_validate(self.buscar(codserv))

    def crear(self, datos: ServicioCreate) -> ServicioRead:
        self.validarnombre(datos.nomserv, None)
        return ServicioRead.model_validate(self.servicios.add(Servicio(**datos.model_dump())))

    def actualizar(self, codserv: int, datos: ServicioCreate) -> ServicioRead:
        servicio = self.buscar(codserv)
        self.validarnombre(datos.nomserv, codserv)
        asignarcampos(servicio, datos)
        return ServicioRead.model_validate(self.servicios.update(servicio))

    def eliminar(self, codserv: int) -> None:
        servicio = self.buscar(codserv)
        if self.personal.existsbyservicio(codserv):
            raise ConflictError("No se puede eliminar un servicio que tiene personal asignado")
        self.servicios.delete(servicio)

    def buscar(self, codserv: int) -> Servicio:
        return obteneroerror(self.servicios, codserv, "El servicio")

    def validarnombre(self, nomserv: str, codserv: int | None) -> None:
        if esotroregistro(self.servicios.getbynombre(nomserv), "codserv", codserv):
            raise ConflictError("Ya existe un servicio con ese nombre")
