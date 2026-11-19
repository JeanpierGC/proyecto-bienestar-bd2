from pathlib import Path

from fastapi import APIRouter, FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.errorhandlers import registerexceptionhandlers
from app.core.permisos import exigirsesion, registrarseguridad
from app.routers import (
    atenciones,
    auditoria,
    auth,
    becas,
    becasotorgadas,
    busquedas,
    citas,
    convocatorias,
    escuelas,
    estudiantes,
    facultades,
    fichas,
    personal,
    postulaciones,
    reglas,
    reportesbecas,
    reportesbienestar,
    reportespostulaciones,
    requisitos,
    resumen,
    seguimientoscaso,
    servicios,
)

FRONTEND = Path(__file__).resolve().parents[2] / "frontend"

app = FastAPI(title="Sistema de Becas y Bienestar Universitario", version="0.1.0")

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)
registerexceptionhandlers(app)
registrarseguridad(app)

api = APIRouter(prefix="/api", dependencies=[Depends(exigirsesion)])
api.include_router(facultades.router)
api.include_router(escuelas.router)
api.include_router(estudiantes.router)
api.include_router(resumen.router)
api.include_router(becas.router)
api.include_router(reglas.router)
api.include_router(requisitos.router)
api.include_router(convocatorias.router)
api.include_router(reportesbecas.router)
api.include_router(becasotorgadas.router)
api.include_router(personal.router)
api.include_router(postulaciones.router)
api.include_router(reportespostulaciones.router)
api.include_router(atenciones.router)
api.include_router(citas.router)
api.include_router(fichas.router)
api.include_router(reportesbienestar.router)
api.include_router(seguimientoscaso.router)
api.include_router(servicios.router)
api.include_router(auditoria.router)
api.include_router(busquedas.router)
api.include_router(auth.router)
app.include_router(api)

# El frontend se sirve desde la misma app: http://localhost:8000/
app.mount("/", StaticFiles(directory=FRONTEND, html=True), name="frontend")
