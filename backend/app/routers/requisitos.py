from fastapi import APIRouter, status

from app.dependencies import RequisitoServiceDep
from app.schemas.requisito import RequisitoCreate, RequisitoRead

router = APIRouter(prefix="/requisitos", tags=["Requisitos"])


@router.get("", response_model=list[RequisitoRead])
def listar(service: RequisitoServiceDep):
    return service.listar()


@router.get("/{codreq}", response_model=RequisitoRead)
def obtener(codreq: int, service: RequisitoServiceDep):
    return service.obtener(codreq)


@router.post("", response_model=RequisitoRead, status_code=status.HTTP_201_CREATED)
def crear(datos: RequisitoCreate, service: RequisitoServiceDep):
    return service.crear(datos)


@router.put("/{codreq}", response_model=RequisitoRead)
def actualizar(codreq: int, datos: RequisitoCreate, service: RequisitoServiceDep):
    return service.actualizar(codreq, datos)


@router.delete("/{codreq}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(codreq: int, service: RequisitoServiceDep):
    service.eliminar(codreq)
