from datetime import date, time
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.referencias import EstudianteResumen, PersonalResumen


class AtencionCreate(BaseModel):
    codcita: int = Field(gt=0)
    resumaten: str = Field(min_length=1)
    recomaten: str | None = None
    nivelaten: Literal["BAJO", "MEDIO", "ALTO", "CRITICO"]
    reqseg: bool = False


class CitaDeAtencion(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    codcita: int
    fechcita: date
    horacita: time
    estudiante: EstudianteResumen
    personal: PersonalResumen


class AtencionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    codaten: int
    resumaten: str
    recomaten: str | None
    nivelaten: str
    reqseg: bool
    codcita: int
    cita: CitaDeAtencion
    cantseguimientos: int = 0


class RiesgoEstudiante(BaseModel):
    codest: int
    nivel: str  # lo calcula la función f5 de la BD
