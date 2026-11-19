from fastapi import APIRouter, status

from app.dependencies import ReglaServiceDep
from app.schemas.regla import ReglaCreate, ReglaRead

router = APIRouter(prefix="/reglas", tags=["Reglas de becas"])


@router.get("", response_model=list[ReglaRead])
def listar(service: ReglaServiceDep, codbeca: int | None = None):
    return service.listar(codbeca)


@router.get("/{codreg}", response_model=ReglaRead)
def obtener(codreg: int, service: ReglaServiceDep):
    return service.obtener(codreg)


@router.post("", response_model=ReglaRead, status_code=status.HTTP_201_CREATED)
def crear(datos: ReglaCreate, service: ReglaServiceDep):
    return service.crear(datos)


@router.put("/{codreg}", response_model=ReglaRead)
def actualizar(codreg: int, datos: ReglaCreate, service: ReglaServiceDep):
    return service.actualizar(codreg, datos)


@router.delete("/{codreg}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(codreg: int, service: ReglaServiceDep):
    service.eliminar(codreg)
