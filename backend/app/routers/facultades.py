from fastapi import APIRouter, status

from app.dependencies import FacultadServiceDep
from app.schemas.facultad import FacultadCreate, FacultadRead

router = APIRouter(prefix="/facultades", tags=["Facultades"])


@router.get("", response_model=list[FacultadRead])
def listar(service: FacultadServiceDep):
    return service.listar()


@router.get("/{codfac}", response_model=FacultadRead)
def obtener(codfac: int, service: FacultadServiceDep):
    return service.obtener(codfac)


@router.post("", response_model=FacultadRead, status_code=status.HTTP_201_CREATED)
def crear(datos: FacultadCreate, service: FacultadServiceDep):
    return service.crear(datos)


@router.put("/{codfac}", response_model=FacultadRead)
def actualizar(codfac: int, datos: FacultadCreate, service: FacultadServiceDep):
    return service.actualizar(codfac, datos)


@router.delete("/{codfac}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(codfac: int, service: FacultadServiceDep):
    service.eliminar(codfac)
