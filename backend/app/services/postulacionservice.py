from datetime import date

from app.core.exceptions import ConflictError
from app.models.postulacion import Postulacion, RequisitoPostulacion
from app.repositories.personalrepository import PersonalRepository
from app.repositories.postulacionrepository import PostulacionRepository
from app.schemas.postulacion import (
    ConteoPostulaciones,
    PostulacionCreate,
    PostulacionEvaluar,
    PostulacionRead,
    RequisitoPresentado,
    RequisitoPresentadoUpdate,
)
from app.services.helpers import obteneroerror
from app.services.procedimientos import exigirmensaje

MENSAJEREGISTRADA = "Postulación registrada"
MENSAJEEVALUADA = "Postulación evaluada"


class PostulacionService:
    def __init__(self, postulaciones: PostulacionRepository, personal: PersonalRepository) -> None:
        self.postulaciones = postulaciones
        self.personal = personal

    def listar(
        self, codest: int | None = None, codconv: int | None = None, estpost: str | None = None
    ) -> list[PostulacionRead]:
        postulaciones = self.postulaciones.listfiltered(codest, codconv, estpost)
        return [self.conmensaje(postulacion) for postulacion in postulaciones]

    def obtener(self, codpost: int) -> PostulacionRead:
        return self.conmensaje(self.buscar(codpost))

    def conteo(self, codest: int) -> ConteoPostulaciones:
        return ConteoPostulaciones(
            codest=codest, cantidad=self.postulaciones.contarporestudiante(codest)
        )

    def registrar(self, datos: PostulacionCreate) -> PostulacionRead:
        mensaje = self.postulaciones.registrar(
            datos.codest, datos.codconv, datos.prompost, datos.ingfampost
        )
        exigirmensaje(mensaje, MENSAJEREGISTRADA)
        creada = self.postulaciones.findbyestudianteconvocatoria(datos.codest, datos.codconv)
        return self.conmensaje(creada)

    def evaluar(self, codpost: int, datos: PostulacionEvaluar) -> PostulacionRead:
        postulacion = self.buscar(codpost)
        if postulacion.otorgada is not None:
            raise ConflictError("La postulación ya tiene una beca otorgada y no se puede reevaluar")
        obteneroerror(self.personal, datos.codpereval, "El evaluador")
        mensaje = self.postulaciones.evaluar(codpost, datos.puntpost, datos.estpost, datos.codpereval)
        exigirmensaje(mensaje, MENSAJEEVALUADA)
        return self.conmensaje(self.buscar(codpost))

    def eliminar(self, codpost: int) -> None:
        postulacion = self.buscar(codpost)
        if postulacion.estpost != "REGISTRADA":
            raise ConflictError("Solo se puede eliminar una postulación que aún no fue evaluada")
        self.postulaciones.delete(postulacion)

    def requisitos(self, codpost: int) -> list[RequisitoPresentado]:
        postulacion = self.buscar(codpost)
        presentados = {item.codreq: item for item in postulacion.requisitos}
        return [self.presentado(requisito, presentados.get(requisito.codreq))
                for requisito in postulacion.convocatoria.beca.requisitos]

    def presentarrequisito(
        self, codpost: int, codreq: int, datos: RequisitoPresentadoUpdate
    ) -> RequisitoPresentado:
        postulacion = self.buscar(codpost)
        requisito = self.requisitodelabeca(postulacion, codreq)
        documento = next((item for item in postulacion.requisitos if item.codreq == codreq), None)
        if documento is None:
            documento = RequisitoPostulacion(codreq=codreq, fechpres=date.today())
            postulacion.requisitos.append(documento)
        documento.estdoc = datos.estdoc
        documento.obsdoc = datos.obsdoc
        self.postulaciones.update(postulacion)
        return self.presentado(requisito, documento)

    def quitarrequisito(self, codpost: int, codreq: int) -> None:
        postulacion = self.buscar(codpost)
        documento = next((item for item in postulacion.requisitos if item.codreq == codreq), None)
        if documento is not None:
            postulacion.requisitos.remove(documento)
            self.postulaciones.update(postulacion)

    def buscar(self, codpost: int) -> Postulacion:
        return obteneroerror(self.postulaciones, codpost, "La postulación")

    def requisitodelabeca(self, postulacion: Postulacion, codreq: int):
        for requisito in postulacion.convocatoria.beca.requisitos:
            if requisito.codreq == codreq:
                return requisito
        raise ConflictError("El requisito no pertenece a la beca de esta postulación")

    def presentado(self, requisito, documento: RequisitoPostulacion | None) -> RequisitoPresentado:
        if documento is None:
            return RequisitoPresentado(codreq=requisito.codreq, nomreq=requisito.nomreq)
        return RequisitoPresentado(
            codreq=requisito.codreq,
            nomreq=requisito.nomreq,
            fechpres=documento.fechpres,
            estdoc=documento.estdoc,
            obsdoc=documento.obsdoc,
        )

    def conmensaje(self, postulacion: Postulacion) -> PostulacionRead:
        lectura = PostulacionRead.model_validate(postulacion)
        lectura.mensajeestado = self.postulaciones.mensajeestado(postulacion.codpost)
        return lectura
