from fastapi import APIRouter

from app.dependencies import ReportePostulacionServiceDep
from app.schemas.reportepostulacion import PostulacionesPorEstudiante, PromedioSeguimientoBeca

router = APIRouter(prefix="/reportes/postulaciones", tags=["Reportes de postulaciones"])


@router.get("/porestudiante", response_model=list[PostulacionesPorEstudiante])
def porestudiante(service: ReportePostulacionServiceDep):
    return service.porestudiante()


@router.get("/promediosbeca", response_model=list[PromedioSeguimientoBeca])
def promediosbeca(service: ReportePostulacionServiceDep):
    return service.promediosbeca()
