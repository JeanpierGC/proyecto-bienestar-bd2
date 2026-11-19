from fastapi import APIRouter, status

from app.dependencies import SeguimientoCasoServiceDep
from app.schemas.seguimientocaso import (
    SeguimientoCasoCreate,
    SeguimientoCasoRead,
    SeguimientoCasoUpdate,
)

router = APIRouter(prefix="/seguimientoscaso", tags=["Seguimiento de casos"])


@router.get("", response_model=list[SeguimientoCasoRead])
def listar(codaten: int, service: SeguimientoCasoServiceDep):
    return service.listar(codaten)


@router.post("", response_model=SeguimientoCasoRead, status_code=status.HTTP_201_CREATED)
def crear(datos: SeguimientoCasoCreate, service: SeguimientoCasoServiceDep):
    return service.crear(datos)


@router.put("/{codseg}", response_model=SeguimientoCasoRead)
def actualizar(codseg: int, datos: SeguimientoCasoUpdate, service: SeguimientoCasoServiceDep):
    return service.actualizar(codseg, datos)


@router.delete("/{codseg}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(codseg: int, service: SeguimientoCasoServiceDep):
    service.eliminar(codseg)
