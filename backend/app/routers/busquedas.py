from fastapi import APIRouter, Query

from app.dependencies import BusquedaServiceDep
from app.schemas.busqueda import EstudianteBusqueda

router = APIRouter(prefix="/busquedas", tags=["Búsquedas"])


@router.get("/estudiantes", response_model=list[EstudianteBusqueda])
def estudiantes(service: BusquedaServiceDep, apellido: str = Query("", max_length=50)):
    return service.estudiantes(apellido)
