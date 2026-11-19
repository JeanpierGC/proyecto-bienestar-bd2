from fastapi import APIRouter

from app.dependencies import ResumenServiceDep
from app.schemas.resumen import ResumenAcademico

router = APIRouter(prefix="/resumen", tags=["Resumen"])


@router.get("/academico", response_model=ResumenAcademico)
def obteneracademico(service: ResumenServiceDep):
    return service.obteneracademico()
