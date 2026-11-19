from fastapi import APIRouter, status

from app.dependencies import ServicioServiceDep
from app.schemas.servicio import ServicioCreate, ServicioRead

router = APIRouter(prefix="/servicios", tags=["Servicios"])


@router.get("", response_model=list[ServicioRead])
def listar(service: ServicioServiceDep):
    return service.listar()


@router.get("/{codserv}", response_model=ServicioRead)
def obtener(codserv: int, service: ServicioServiceDep):
    return service.obtener(codserv)


@router.post("", response_model=ServicioRead, status_code=status.HTTP_201_CREATED)
def crear(datos: ServicioCreate, service: ServicioServiceDep):
    return service.crear(datos)


@router.put("/{codserv}", response_model=ServicioRead)
def actualizar(codserv: int, datos: ServicioCreate, service: ServicioServiceDep):
    return service.actualizar(codserv, datos)


@router.delete("/{codserv}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(codserv: int, service: ServicioServiceDep):
    service.eliminar(codserv)
