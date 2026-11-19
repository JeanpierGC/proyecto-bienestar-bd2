from datetime import date, time
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.referencias import EstudianteResumen, PersonalResumen


class CitaCreate(BaseModel):
    codest: int = Field(gt=0)
    codper: int = Field(gt=0)
    fechcita: date
    horacita: time
    modcita: Literal["PRESENCIAL", "VIRTUAL"]
    motcita: str | None = Field(default=None, max_length=200)

    @field_validator("fechcita")
    @classmethod
    def fechanopasada(cls, fecha: date) -> date:
        if fecha < date.today():
            raise ValueError("La fecha de la cita no puede ser pasada")
        return fecha


class CitaEstado(BaseModel):
    """Una cita solo se cancela o se marca como no asistida; 'atendida' la pone la atención."""

    estcita: Literal["CANCELADA", "NO_ASISTIO"]


class AtencionDeCita(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    codaten: int
    nivelaten: str


class CitaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    codcita: int
    fechcita: date
    horacita: time
    modcita: str
    motcita: str | None
    estcita: str
    codest: int
    codper: int
    estudiante: EstudianteResumen
    personal: PersonalResumen
    atencion: AtencionDeCita | None
