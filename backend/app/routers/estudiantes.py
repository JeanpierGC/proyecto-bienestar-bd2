from fastapi import APIRouter, status

from app.dependencies import EstudianteServiceDep
from app.schemas.estudiante import EstudianteCreate, EstudianteRead

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])


@router.get("", response_model=list[EstudianteRead])
def listar(service: EstudianteServiceDep, codesc: int | None = None):
    return service.listar(codesc)


@router.get("/{codest}", response_model=EstudianteRead)
def obtener(codest: int, service: EstudianteServiceDep):
    return service.obtener(codest)


@router.post("", response_model=EstudianteRead, status_code=status.HTTP_201_CREATED)
def crear(datos: EstudianteCreate, service: EstudianteServiceDep):
    return service.crear(datos)


@router.put("/{codest}", response_model=EstudianteRead)
def actualizar(codest: int, datos: EstudianteCreate, service: EstudianteServiceDep):
    return service.actualizar(codest, datos)


@router.delete("/{codest}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(codest: int, service: EstudianteServiceDep):
    service.eliminar(codest)
