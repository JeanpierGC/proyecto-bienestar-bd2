from fastapi import APIRouter, status

from app.dependencies import ConvocatoriaServiceDep
from app.schemas.convocatoria import ConvocatoriaCreate, ConvocatoriaRead

router = APIRouter(prefix="/convocatorias", tags=["Convocatorias"])


@router.get("", response_model=list[ConvocatoriaRead])
def listar(service: ConvocatoriaServiceDep, codbeca: int | None = None):
    return service.listar(codbeca)


@router.get("/{codconv}", response_model=ConvocatoriaRead)
def obtener(codconv: int, service: ConvocatoriaServiceDep):
    return service.obtener(codconv)


@router.post("", response_model=ConvocatoriaRead, status_code=status.HTTP_201_CREATED)
def crear(datos: ConvocatoriaCreate, service: ConvocatoriaServiceDep):
    return service.crear(datos)


@router.put("/{codconv}", response_model=ConvocatoriaRead)
def actualizar(codconv: int, datos: ConvocatoriaCreate, service: ConvocatoriaServiceDep):
    return service.actualizar(codconv, datos)


@router.delete("/{codconv}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(codconv: int, service: ConvocatoriaServiceDep):
    service.eliminar(codconv)
