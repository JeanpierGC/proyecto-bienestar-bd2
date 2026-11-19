from fastapi import APIRouter, status

from app.dependencies import AtencionServiceDep
from app.schemas.atencion import AtencionCreate, AtencionRead, RiesgoEstudiante

router = APIRouter(prefix="/atenciones", tags=["Atenciones"])


@router.get("", response_model=list[AtencionRead])
def listar(service: AtencionServiceDep, codest: int | None = None):
    return service.listar(codest)


@router.get("/riesgo/{codest}", response_model=RiesgoEstudiante)
def riesgo(codest: int, service: AtencionServiceDep):
    return service.riesgo(codest)


@router.get("/{codaten}", response_model=AtencionRead)
def obtener(codaten: int, service: AtencionServiceDep):
    return service.obtener(codaten)


@router.post("", response_model=AtencionRead, status_code=status.HTTP_201_CREATED)
def registrar(datos: AtencionCreate, service: AtencionServiceDep):
    return service.registrar(datos)
