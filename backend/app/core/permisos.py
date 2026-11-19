"""Quién puede hacer qué. Un administrador puede todo; un estudiante solo ve y gestiona lo suyo."""

import re

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import getdb
from app.core.seguridad import CredencialesError, leertoken
from app.schemas.auth import UsuarioActual

RUTALOGIN = "/api/auth/login"

# Catálogos que cualquier estudiante puede consultar (solo lectura).
CATALOGOS = re.compile(r"^/api/(becas|convocatorias|reglas|requisitos|servicios|personal)(/.*)?$")
# Listados que traen datos de varios estudiantes: el estudiante debe pedir solo los suyos (?codest=).
LISTADOSPROPIOS = {"/api/postulaciones", "/api/citas", "/api/becasotorgadas", "/api/atenciones"}
# Consultas por código de estudiante en la ruta.
PORESTUDIANTE = re.compile(r"^/api/(?:postulaciones/conteo|atenciones/riesgo)/(\d+)$")
# Recursos con código propio: (patrón, métodos permitidos, tabla que dice de quién es)
RECURSOS = [
    (re.compile(r"^/api/postulaciones/(\d+)$"), {"GET", "DELETE"}, "postulacion"),
    (re.compile(r"^/api/postulaciones/(\d+)/requisitos$"), {"GET"}, "postulacion"),
    (re.compile(r"^/api/postulaciones/(\d+)/requisitos/\d+$"), {"PUT"}, "postulacion"),
    (re.compile(r"^/api/citas/(\d+)$"), {"GET"}, "cita"),
    (re.compile(r"^/api/citas/(\d+)/estado$"), {"PUT"}, "cita"),
    (re.compile(r"^/api/becasotorgadas/(\d+)$"), {"GET"}, "otorgada"),
    (re.compile(r"^/api/becasotorgadas/(\d+)/seguimientos$"), {"GET"}, "otorgada"),
    (re.compile(r"^/api/atenciones/(\d+)$"), {"GET"}, "atencion"),
]
# Consulta que devuelve el estudiante dueño de cada recurso.
DUENOS = {
    "postulacion": "select codest from Postulacion where codpost = :id",
    "cita": "select codest from Cita where codcita = :id",
    "otorgada": "select p.codest from BecaOtorgada b join Postulacion p on b.codpost = p.codpost where b.codotor = :id",
    "atencion": "select c.codest from Atencion a join Cita c on a.codcita = c.codcita where a.codaten = :id",
}


def noautorizado(mensaje: str = "Tu sesión venció o no es válida. Vuelve a iniciar sesión.") -> HTTPException:
    return HTTPException(status.HTTP_401_UNAUTHORIZED, mensaje)


def prohibido() -> HTTPException:
    return HTTPException(status.HTTP_403_FORBIDDEN, "No tienes permiso para esta acción")


def leersesion(request: Request) -> UsuarioActual:
    cabecera = request.headers.get("Authorization", "")
    datos = leertoken(cabecera[7:]) if cabecera.startswith("Bearer ") else None
    if datos is None:
        raise noautorizado()
    return UsuarioActual(codusu=datos["codusu"], rolusu=datos["rolusu"], codest=datos["codest"])


def dueno(db: Session, recurso: str, codigo: int) -> int | None:
    return db.execute(text(DUENOS[recurso]), {"id": codigo}).scalar()


async def cuerpocodest(request: Request) -> int | None:
    try:
        return (await request.json()).get("codest")
    except (ValueError, AttributeError):
        return None


async def estudiantepermitido(request: Request, sesion: UsuarioActual, db: Session) -> bool:
    metodo, ruta, propio = request.method, request.url.path, sesion.codest
    if ruta in {"/api/auth/yo", "/api/auth/perfil", "/api/auth/clave"}:
        return True
    if metodo == "GET" and CATALOGOS.match(ruta):
        return True
    if metodo == "GET" and ruta in LISTADOSPROPIOS:
        return request.query_params.get("codest") == str(propio)
    if metodo == "GET" and (coincide := PORESTUDIANTE.match(ruta)):
        return int(coincide.group(1)) == propio
    if metodo == "POST" and ruta in {"/api/postulaciones", "/api/citas"}:
        return await cuerpocodest(request) == propio
    if metodo == "GET" and ruta == "/api/seguimientoscaso":
        codaten = request.query_params.get("codaten", "")
        return codaten.isdigit() and dueno(db, "atencion", int(codaten)) in (propio, None)
    for patron, metodos, recurso in RECURSOS:
        if (coincide := patron.match(ruta)) and metodo in metodos:
            # Si el código no existe, se deja pasar para que la API responda 404.
            return dueno(db, recurso, int(coincide.group(1))) in (propio, None)
    return False


async def exigirsesion(request: Request, db: Session = Depends(getdb)) -> UsuarioActual:
    """Se aplica a toda la API: sin sesión válida no se entra, salvo al login."""
    if request.url.path == RUTALOGIN:
        return None
    sesion = leersesion(request)
    request.state.sesion = sesion
    if sesion.rolusu != "ADMIN" and not await estudiantepermitido(request, sesion, db):
        raise prohibido()
    return sesion


def registrarseguridad(app: FastAPI) -> None:
    async def credenciales(_: Request, exc: CredencialesError) -> JSONResponse:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": exc.message})

    app.add_exception_handler(CredencialesError, credenciales)
