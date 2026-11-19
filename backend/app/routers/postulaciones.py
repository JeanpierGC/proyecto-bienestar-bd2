from fastapi import APIRouter, status

from app.dependencies import PostulacionServiceDep
from app.schemas.postulacion import (
    ConteoPostulaciones,
    PostulacionCreate,
    PostulacionEvaluar,
    PostulacionRead,
    RequisitoPresentado,
    RequisitoPresentadoUpdate,
)

router = APIRouter(prefix="/postulaciones", tags=["Postulaciones"])


@router.get("", response_model=list[PostulacionRead])
def listar(
    service: PostulacionServiceDep,
    codest: int | None = None,
    codconv: int | None = None,
    estpost: str | None = None,
):
    return service.listar(codest, codconv, estpost)


@router.get("/conteo/{codest}", response_model=ConteoPostulaciones)
def conteo(codest: int, service: PostulacionServiceDep):
    return service.conteo(codest)


@router.get("/{codpost}", response_model=PostulacionRead)
def obtener(codpost: int, service: PostulacionServiceDep):
    return service.obtener(codpost)


@router.post("", response_model=PostulacionRead, status_code=status.HTTP_201_CREATED)
def registrar(datos: PostulacionCreate, service: PostulacionServiceDep):
    return service.registrar(datos)


@router.put("/{codpost}/evaluacion", response_model=PostulacionRead)
def evaluar(codpost: int, datos: PostulacionEvaluar, service: PostulacionServiceDep):
    return service.evaluar(codpost, datos)


@router.delete("/{codpost}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(codpost: int, service: PostulacionServiceDep):
    service.eliminar(codpost)


@router.get("/{codpost}/requisitos", response_model=list[RequisitoPresentado])
def requisitos(codpost: int, service: PostulacionServiceDep):
    return service.requisitos(codpost)


@router.put("/{codpost}/requisitos/{codreq}", response_model=RequisitoPresentado)
def presentarrequisito(
    codpost: int, codreq: int, datos: RequisitoPresentadoUpdate, service: PostulacionServiceDep
):
    return service.presentarrequisito(codpost, codreq, datos)


@router.delete("/{codpost}/requisitos/{codreq}", status_code=status.HTTP_204_NO_CONTENT)
def quitarrequisito(codpost: int, codreq: int, service: PostulacionServiceDep):
    service.quitarrequisito(codpost, codreq)
