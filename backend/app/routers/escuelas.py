from fastapi import APIRouter, status

from app.dependencies import EscuelaServiceDep
from app.schemas.escuela import EscuelaCreate, EscuelaRead

router = APIRouter(prefix="/escuelas", tags=["Escuelas"])


@router.get("", response_model=list[EscuelaRead])
def listar(service: EscuelaServiceDep, codfac: int | None = None):
    return service.listar(codfac)


@router.get("/{codesc}", response_model=EscuelaRead)
def obtener(codesc: int, service: EscuelaServiceDep):
    return service.obtener(codesc)


@router.post("", response_model=EscuelaRead, status_code=status.HTTP_201_CREATED)
def crear(datos: EscuelaCreate, service: EscuelaServiceDep):
    return service.crear(datos)


@router.put("/{codesc}", response_model=EscuelaRead)
def actualizar(codesc: int, datos: EscuelaCreate, service: EscuelaServiceDep):
    return service.actualizar(codesc, datos)


@router.delete("/{codesc}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(codesc: int, service: EscuelaServiceDep):
    service.eliminar(codesc)
