from fastapi import APIRouter

from app.dependencies import AuditoriaServiceDep
from app.schemas.auditoria import RegistroAuditoria

router = APIRouter(prefix="/auditoria", tags=["Auditoría"])


@router.get("/postulaciones", response_model=list[RegistroAuditoria])
def postulaciones(service: AuditoriaServiceDep):
    return service.postulaciones()


@router.get("/otorgamientos", response_model=list[RegistroAuditoria])
def otorgamientos(service: AuditoriaServiceDep):
    return service.otorgamientos()


@router.get("/citas", response_model=list[RegistroAuditoria])
def citas(service: AuditoriaServiceDep):
    return service.citas()
