from fastapi import APIRouter, status

from app.dependencies import CitaServiceDep
from app.schemas.cita import CitaCreate, CitaEstado, CitaRead

router = APIRouter(prefix="/citas", tags=["Citas"])


@router.get("", response_model=list[CitaRead])
def listar(
    service: CitaServiceDep,
    codest: int | None = None,
    codper: int | None = None,
    estcita: str | None = None,
):
    return service.listar(codest, codper, estcita)


@router.get("/{codcita}", response_model=CitaRead)
def obtener(codcita: int, service: CitaServiceDep):
    return service.obtener(codcita)


@router.post("", response_model=CitaRead, status_code=status.HTTP_201_CREATED)
def registrar(datos: CitaCreate, service: CitaServiceDep):
    return service.registrar(datos)


@router.put("/{codcita}/estado", response_model=CitaRead)
def cambiarestado(codcita: int, datos: CitaEstado, service: CitaServiceDep):
    return service.cambiarestado(codcita, datos)


@router.delete("/{codcita}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(codcita: int, service: CitaServiceDep):
    service.eliminar(codcita)
