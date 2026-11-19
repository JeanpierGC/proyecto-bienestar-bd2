from fastapi import APIRouter, status

from app.dependencies import FichaPsicologicaServiceDep
from app.schemas.fichapsicologica import FichaCreate, FichaRead

router = APIRouter(prefix="/fichas", tags=["Fichas psicológicas"])


@router.get("", response_model=list[FichaRead])
def listar(service: FichaPsicologicaServiceDep, codest: int | None = None):
    return service.listar(codest)


@router.get("/{codfic}", response_model=FichaRead)
def obtener(codfic: int, service: FichaPsicologicaServiceDep):
    return service.obtener(codfic)


@router.post("", response_model=FichaRead, status_code=status.HTTP_201_CREATED)
def crear(datos: FichaCreate, service: FichaPsicologicaServiceDep):
    return service.crear(datos)


@router.put("/{codfic}", response_model=FichaRead)
def actualizar(codfic: int, datos: FichaCreate, service: FichaPsicologicaServiceDep):
    return service.actualizar(codfic, datos)


@router.delete("/{codfic}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(codfic: int, service: FichaPsicologicaServiceDep):
    service.eliminar(codfic)
