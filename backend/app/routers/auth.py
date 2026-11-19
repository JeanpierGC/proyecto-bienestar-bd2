from fastapi import APIRouter, Request, status

from app.dependencies import AuthServiceDep
from app.schemas.auth import CambioClave, LoginIn, PerfilOut, SesionOut

router = APIRouter(prefix="/auth", tags=["Acceso"])


@router.post("/login", response_model=SesionOut)
def login(datos: LoginIn, service: AuthServiceDep):
    return service.login(datos)


@router.get("/yo")
def yo(request: Request):
    """Devuelve quién es el usuario del token (sirve para comprobar que la sesión sigue vigente)."""
    sesion = request.state.sesion
    return {"codusu": sesion.codusu, "rolusu": sesion.rolusu, "codest": sesion.codest}


@router.get("/perfil", response_model=PerfilOut)
def perfil(request: Request, service: AuthServiceDep):
    return service.perfil(request.state.sesion.codusu)


@router.put("/clave", status_code=status.HTTP_204_NO_CONTENT)
def cambiarclave(datos: CambioClave, request: Request, service: AuthServiceDep):
    service.cambiarclave(request.state.sesion.codusu, datos)
