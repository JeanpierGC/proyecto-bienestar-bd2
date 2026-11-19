"""Punto único donde se conectan los services con sus repositorios concretos."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import getdb
from app.repositories.becarepository import SQLAlchemyBecaRepository
from app.repositories.convocatoriarepository import SQLAlchemyConvocatoriaRepository
from app.repositories.escuelarepository import SQLAlchemyEscuelaRepository
from app.repositories.estudianterepository import SQLAlchemyEstudianteRepository
from app.repositories.facultadrepository import SQLAlchemyFacultadRepository
from app.repositories.reglarepository import SQLAlchemyReglaRepository
from app.repositories.reportebecarepository import SQLAlchemyReporteBecaRepository
from app.repositories.requisitorepository import SQLAlchemyRequisitoRepository
from app.services.becaservice import BecaService
from app.services.convocatoriaservice import ConvocatoriaService
from app.services.escuelaservice import EscuelaService
from app.services.estudianteservice import EstudianteService
from app.services.facultadservice import FacultadService
from app.services.reglaservice import ReglaService
from app.services.reportebecaservice import ReporteBecaService
from app.services.requisitoservice import RequisitoService
from app.services.resumenservice import ResumenService
from app.repositories.becaotorgadarepository import (
    SQLAlchemyBecaOtorgadaRepository,
    SQLAlchemySeguimientoBecaRepository,
)
from app.repositories.personalrepository import SQLAlchemyPersonalRepository
from app.repositories.postulacionrepository import SQLAlchemyPostulacionRepository
from app.repositories.reportepostulacionrepository import SQLAlchemyReportePostulacionRepository
from app.services.becaotorgadaservice import BecaOtorgadaService
from app.services.personalservice import PersonalService
from app.services.postulacionservice import PostulacionService
from app.services.reportepostulacionservice import ReportePostulacionService

from app.repositories.atencionrepository import SQLAlchemyAtencionRepository
from app.repositories.citarepository import SQLAlchemyCitaRepository
from app.repositories.fichapsicologicarepository import SQLAlchemyFichaPsicologicaRepository
from app.repositories.reportebienestarrepository import SQLAlchemyReporteBienestarRepository
from app.repositories.seguimientocasorepository import SQLAlchemySeguimientoCasoRepository
from app.repositories.serviciorepository import SQLAlchemyServicioRepository
from app.services.atencionservice import AtencionService
from app.services.citaservice import CitaService
from app.services.fichapsicologicaservice import FichaPsicologicaService
from app.services.reportebienestarservice import ReporteBienestarService
from app.services.seguimientocasoservice import SeguimientoCasoService
from app.services.servicioservice import ServicioService

from app.repositories.auditoriarepository import SQLAlchemyAuditoriaRepository
from app.services.auditoriaservice import AuditoriaService

from app.repositories.busquedarepository import SQLAlchemyBusquedaRepository
from app.services.busquedaservice import BusquedaService

from app.repositories.usuariorepository import SQLAlchemyUsuarioRepository
from app.services.authservice import AuthService

DbSession = Annotated[Session, Depends(getdb)]


# ---------- Módulo Académico ----------
def getfacultadservice(db: DbSession) -> FacultadService:
    return FacultadService(SQLAlchemyFacultadRepository(db), SQLAlchemyEscuelaRepository(db))


def getescuelaservice(db: DbSession) -> EscuelaService:
    return EscuelaService(
        SQLAlchemyEscuelaRepository(db),
        SQLAlchemyFacultadRepository(db),
        SQLAlchemyEstudianteRepository(db),
    )


def getestudianteservice(db: DbSession) -> EstudianteService:
    return EstudianteService(SQLAlchemyEstudianteRepository(db), SQLAlchemyEscuelaRepository(db))


def getresumenservice(db: DbSession) -> ResumenService:
    return ResumenService(
        SQLAlchemyFacultadRepository(db),
        SQLAlchemyEscuelaRepository(db),
        SQLAlchemyEstudianteRepository(db),
    )


# ---------- Módulo Becas ----------
def getbecaservice(db: DbSession) -> BecaService:
    return BecaService(
        SQLAlchemyBecaRepository(db),
        SQLAlchemyConvocatoriaRepository(db),
        SQLAlchemyRequisitoRepository(db),
    )


def getreglaservice(db: DbSession) -> ReglaService:
    return ReglaService(SQLAlchemyReglaRepository(db), SQLAlchemyBecaRepository(db))


def getrequisitoservice(db: DbSession) -> RequisitoService:
    return RequisitoService(SQLAlchemyRequisitoRepository(db))


def getconvocatoriaservice(db: DbSession) -> ConvocatoriaService:
    return ConvocatoriaService(SQLAlchemyConvocatoriaRepository(db), SQLAlchemyBecaRepository(db))


def getreportebecaservice(db: DbSession) -> ReporteBecaService:
    return ReporteBecaService(SQLAlchemyReporteBecaRepository(db))


FacultadServiceDep = Annotated[FacultadService, Depends(getfacultadservice)]
EscuelaServiceDep = Annotated[EscuelaService, Depends(getescuelaservice)]
EstudianteServiceDep = Annotated[EstudianteService, Depends(getestudianteservice)]
ResumenServiceDep = Annotated[ResumenService, Depends(getresumenservice)]
BecaServiceDep = Annotated[BecaService, Depends(getbecaservice)]
ReglaServiceDep = Annotated[ReglaService, Depends(getreglaservice)]
RequisitoServiceDep = Annotated[RequisitoService, Depends(getrequisitoservice)]
ConvocatoriaServiceDep = Annotated[ConvocatoriaService, Depends(getconvocatoriaservice)]
ReporteBecaServiceDep = Annotated[ReporteBecaService, Depends(getreportebecaservice)]


def getpersonalservice(db: DbSession) -> PersonalService:
    return PersonalService(SQLAlchemyPersonalRepository(db), SQLAlchemyServicioRepository(db))


def getpostulacionservice(db: DbSession) -> PostulacionService:
    return PostulacionService(SQLAlchemyPostulacionRepository(db), SQLAlchemyPersonalRepository(db))


def getbecaotorgadaservice(db: DbSession) -> BecaOtorgadaService:
    return BecaOtorgadaService(
        SQLAlchemyBecaOtorgadaRepository(db),
        SQLAlchemySeguimientoBecaRepository(db),
        SQLAlchemyPersonalRepository(db),
    )


def getreportepostulacionservice(db: DbSession) -> ReportePostulacionService:
    return ReportePostulacionService(SQLAlchemyReportePostulacionRepository(db))


PersonalServiceDep = Annotated[PersonalService, Depends(getpersonalservice)]
PostulacionServiceDep = Annotated[PostulacionService, Depends(getpostulacionservice)]
BecaOtorgadaServiceDep = Annotated[BecaOtorgadaService, Depends(getbecaotorgadaservice)]
ReportePostulacionServiceDep = Annotated[
    ReportePostulacionService, Depends(getreportepostulacionservice)
]


def getservicioservice(db: DbSession) -> ServicioService:
    return ServicioService(SQLAlchemyServicioRepository(db), SQLAlchemyPersonalRepository(db))


def getcitaservice(db: DbSession) -> CitaService:
    return CitaService(
        SQLAlchemyCitaRepository(db), SQLAlchemyEstudianteRepository(db), SQLAlchemyPersonalRepository(db)
    )


def getatencionservice(db: DbSession) -> AtencionService:
    return AtencionService(SQLAlchemyAtencionRepository(db))


def getseguimientocasoservice(db: DbSession) -> SeguimientoCasoService:
    return SeguimientoCasoService(SQLAlchemySeguimientoCasoRepository(db), SQLAlchemyAtencionRepository(db))


def getfichapsicologicaservice(db: DbSession) -> FichaPsicologicaService:
    return FichaPsicologicaService(
        SQLAlchemyFichaPsicologicaRepository(db),
        SQLAlchemyEstudianteRepository(db),
        SQLAlchemyPersonalRepository(db),
    )


def getreportebienestarservice(db: DbSession) -> ReporteBienestarService:
    return ReporteBienestarService(SQLAlchemyReporteBienestarRepository(db))


ServicioServiceDep = Annotated[ServicioService, Depends(getservicioservice)]
CitaServiceDep = Annotated[CitaService, Depends(getcitaservice)]
AtencionServiceDep = Annotated[AtencionService, Depends(getatencionservice)]
SeguimientoCasoServiceDep = Annotated[SeguimientoCasoService, Depends(getseguimientocasoservice)]
FichaPsicologicaServiceDep = Annotated[FichaPsicologicaService, Depends(getfichapsicologicaservice)]
ReporteBienestarServiceDep = Annotated[ReporteBienestarService, Depends(getreportebienestarservice)]


def getauditoriaservice(db: DbSession) -> AuditoriaService:
    return AuditoriaService(SQLAlchemyAuditoriaRepository(db))


AuditoriaServiceDep = Annotated[AuditoriaService, Depends(getauditoriaservice)]


def getbusquedaservice(db: DbSession) -> BusquedaService:
    return BusquedaService(SQLAlchemyBusquedaRepository(db))


BusquedaServiceDep = Annotated[BusquedaService, Depends(getbusquedaservice)]


def getauthservice(db: DbSession) -> AuthService:
    return AuthService(SQLAlchemyUsuarioRepository(db))


AuthServiceDep = Annotated[AuthService, Depends(getauthservice)]
