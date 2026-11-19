from fastapi import APIRouter, Query

from app.dependencies import ReporteBecaServiceDep
from app.schemas.reportebeca import BecaOtorgadaPorConvocatoria, CuposConvocatoria, RankingBeca

router = APIRouter(prefix="/reportes/becas", tags=["Reportes de becas"])


@router.get("/otorgadas", response_model=list[BecaOtorgadaPorConvocatoria])
def otorgadas(service: ReporteBecaServiceDep):
    return service.otorgadasconv()


@router.get("/cuposconv", response_model=list[CuposConvocatoria])
def cuposconv(service: ReporteBecaServiceDep):
    return service.cuposconv()


@router.get("/ranking", response_model=list[RankingBeca])
def ranking(service: ReporteBecaServiceDep, anio: int = Query(ge=2000, le=2100)):
    return service.rankingbecas(anio)
