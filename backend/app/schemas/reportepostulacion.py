from pydantic import BaseModel


class PostulacionesPorEstudiante(BaseModel):
    """Fila de la vista v01."""

    estudiante: str
    anio: int
    cantpostulaciones: int


class PromedioSeguimientoBeca(BaseModel):
    """Fila de la vista v05."""

    beca: str
    promedio: float
    cantseguimientos: int
