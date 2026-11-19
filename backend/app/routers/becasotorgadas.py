from fastapi import APIRouter, status

from app.dependencies import BecaOtorgadaServiceDep
from app.schemas.becaotorgada import (
    BecaOtorgadaCreate,
    BecaOtorgadaEstado,
    BecaOtorgadaRead,
    SeguimientoBecaCreate,
    SeguimientoBecaRead,
)

router = APIRouter(prefix="/becasotorgadas", tags=["Becas otorgadas"])


@router.get("", response_model=list[BecaOtorgadaRead])
def listar(service: BecaOtorgadaServiceDep, codest: int | None = None):
    return service.listar(codest)


@router.get("/{codotor}", response_model=BecaOtorgadaRead)
def obtener(codotor: int, service: BecaOtorgadaServiceDep):
    return service.obtener(codotor)


@router.post("", response_model=BecaOtorgadaRead, status_code=status.HTTP_201_CREATED)
def otorgar(datos: BecaOtorgadaCreate, service: BecaOtorgadaServiceDep):
    return service.otorgar(datos)


@router.put("/{codotor}/estado", response_model=BecaOtorgadaRead)
def cambiarestado(codotor: int, datos: BecaOtorgadaEstado, service: BecaOtorgadaServiceDep):
    return service.cambiarestado(codotor, datos)


@router.delete("/{codotor}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(codotor: int, service: BecaOtorgadaServiceDep):
    service.eliminar(codotor)


@router.get("/{codotor}/seguimientos", response_model=list[SeguimientoBecaRead])
def listarseguimientos(codotor: int, service: BecaOtorgadaServiceDep):
    return service.listarseguimientos(codotor)


@router.post(
    "/{codotor}/seguimientos",
    response_model=SeguimientoBecaRead,
    status_code=status.HTTP_201_CREATED,
)
def registrarseguimiento(
    codotor: int, datos: SeguimientoBecaCreate, service: BecaOtorgadaServiceDep
):
    return service.registrarseguimiento(codotor, datos)


@router.delete("/{codotor}/seguimientos/{codsegb}", status_code=status.HTTP_204_NO_CONTENT)
def eliminarseguimiento(codotor: int, codsegb: int, service: BecaOtorgadaServiceDep):
    service.eliminarseguimiento(codotor, codsegb)
