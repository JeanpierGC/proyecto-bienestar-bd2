from fastapi import APIRouter, status

from app.dependencies import BecaServiceDep
from app.schemas.beca import BecaCreate, BecaRead, BecaRequisitosUpdate

router = APIRouter(prefix="/becas", tags=["Becas"])


@router.get("", response_model=list[BecaRead])
def listar(service: BecaServiceDep):
    return service.listar()


@router.get("/{codbeca}", response_model=BecaRead)
def obtener(codbeca: int, service: BecaServiceDep):
    return service.obtener(codbeca)


@router.post("", response_model=BecaRead, status_code=status.HTTP_201_CREATED)
def crear(datos: BecaCreate, service: BecaServiceDep):
    return service.crear(datos)


@router.put("/{codbeca}", response_model=BecaRead)
def actualizar(codbeca: int, datos: BecaCreate, service: BecaServiceDep):
    return service.actualizar(codbeca, datos)


@router.put("/{codbeca}/requisitos", response_model=BecaRead)
def asignarrequisitos(codbeca: int, datos: BecaRequisitosUpdate, service: BecaServiceDep):
    return service.asignarrequisitos(codbeca, datos)


@router.delete("/{codbeca}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(codbeca: int, service: BecaServiceDep):
    service.eliminar(codbeca)
