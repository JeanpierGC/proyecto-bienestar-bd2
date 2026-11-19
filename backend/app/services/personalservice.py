from app.core.exceptions import ConflictError
from app.models.personal import Personal
from app.repositories.personalrepository import PersonalRepository
from app.repositories.serviciorepository import ServicioRepository
from app.schemas.personal import PersonalCreate, PersonalRead
from app.services.helpers import asignarcampos, esotroregistro, obteneroerror


class PersonalService:
    def __init__(self, personal: PersonalRepository, servicios: ServicioRepository) -> None:
        self.personal = personal
        self.servicios = servicios

    def listar(self) -> list[PersonalRead]:
        return [PersonalRead.model_validate(persona) for persona in self.personal.listall()]

    def obtener(self, codper: int) -> PersonalRead:
        return PersonalRead.model_validate(self.buscar(codper))

    def crear(self, datos: PersonalCreate) -> PersonalRead:
        self.validar(datos, None)
        return PersonalRead.model_validate(self.personal.add(Personal(**datos.model_dump())))

    def actualizar(self, codper: int, datos: PersonalCreate) -> PersonalRead:
        persona = self.buscar(codper)
        self.validar(datos, codper)
        asignarcampos(persona, datos)
        return PersonalRead.model_validate(self.personal.update(persona))

    def eliminar(self, codper: int) -> None:
        self.personal.delete(self.buscar(codper))

    def buscar(self, codper: int) -> Personal:
        return obteneroerror(self.personal, codper, "El personal")

    def validar(self, datos: PersonalCreate, codper: int | None) -> None:
        obteneroerror(self.servicios, datos.codserv, "El servicio")
        if esotroregistro(self.personal.getbydni(datos.dniper), "codper", codper):
            raise ConflictError("Ya existe personal con ese DNI")
        if esotroregistro(self.personal.getbycorreo(datos.corrper), "codper", codper):
            raise ConflictError("Ya existe personal con ese correo")
