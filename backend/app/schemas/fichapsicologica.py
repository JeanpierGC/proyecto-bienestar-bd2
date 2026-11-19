from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.referencias import EstudianteResumen, PersonalResumen


class FichaCreate(BaseModel):
    """Obligatorios: fecha, motivo, estudiante y responsable. Diagnóstico y plan se completan después."""

    fechaper: date
    motfic: str = Field(min_length=1)
    antfic: str | None = None
    diagfic: str | None = None
    planfic: str | None = None
    estfic: Literal["ABIERTA", "CERRADA"] = "ABIERTA"
    codest: int = Field(gt=0)
    codperresp: int = Field(gt=0)


class FichaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    codfic: int
    fechaper: date
    motfic: str
    antfic: str | None
    diagfic: str | None
    planfic: str | None
    estfic: str
    codest: int
    codperresp: int
    estudiante: EstudianteResumen
    responsable: PersonalResumen
