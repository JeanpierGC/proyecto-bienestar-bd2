from fastapi import APIRouter, status

from app.dependencies import PersonalServiceDep
from app.schemas.personal import PersonalCreate, PersonalRead

router = APIRouter(prefix="/personal", tags=["Personal"])


@router.get("", response_model=list[PersonalRead])
def listar(service: PersonalServiceDep):
    return service.listar()


@router.get("/{codper}", response_model=PersonalRead)
def obtener(codper: int, service: PersonalServiceDep):
    return service.obtener(codper)


@router.post("", response_model=PersonalRead, status_code=status.HTTP_201_CREATED)
def crear(datos: PersonalCreate, service: PersonalServiceDep):
    return service.crear(datos)


@router.put("/{codper}", response_model=PersonalRead)
def actualizar(codper: int, datos: PersonalCreate, service: PersonalServiceDep):
    return service.actualizar(codper, datos)


@router.delete("/{codper}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(codper: int, service: PersonalServiceDep):
    service.eliminar(codper)
