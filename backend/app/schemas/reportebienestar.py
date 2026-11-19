from datetime import date

from pydantic import BaseModel


class CitasPorProfesional(BaseModel):
    """Fila de la vista v03."""

    profesional: str
    servicio: str
    cantcitas: int


class CasoRiesgo(BaseModel):
    """Fila de la vista v04."""

    estudiante: str
    fechacita: date
    nivel: str
    estadoseguimiento: str
    proximafecha: date | None
