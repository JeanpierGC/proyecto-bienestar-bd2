from pydantic import BaseModel

from app.schemas.estudiante import EstudianteRead


class EscuelaConteo(BaseModel):
    codesc: int
    nomesc: str
    nomfac: str
    total: int


class CicloConteo(BaseModel):
    ciclo: int
    total: int


class ResumenAcademico(BaseModel):
    totalfacultades: int
    totalescuelas: int
    totalestudiantes: int
    ciclopromedio: float | None
    estudiantesporescuela: list[EscuelaConteo]
    estudiantesporciclo: list[CicloConteo]
    ultimosestudiantes: list[EstudianteRead]
