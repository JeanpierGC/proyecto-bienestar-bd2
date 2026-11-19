from fastapi import APIRouter

from app.dependencies import ReporteBienestarServiceDep
from app.schemas.reportebienestar import CasoRiesgo, CitasPorProfesional

router = APIRouter(prefix="/reportes/bienestar", tags=["Reportes de bienestar"])


@router.get("/citasprofesional", response_model=list[CitasPorProfesional])
def citasprofesional(service: ReporteBienestarServiceDep):
    return service.citasprofesional()


@router.get("/casosriesgo", response_model=list[CasoRiesgo])
def casosriesgo(service: ReporteBienestarServiceDep):
    return service.casosriesgo()
