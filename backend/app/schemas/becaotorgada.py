from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schemas.referencias import ConvocatoriaResumen, EstudianteResumen, PersonalResumen


class BecaOtorgadaCreate(BaseModel):
    codpost: int = Field(gt=0)
    fechiniotor: date
    fechfinotor: date

    @model_validator(mode="after")
    def validarfechas(self) -> "BecaOtorgadaCreate":
        if self.fechfinotor <= self.fechiniotor:
            raise ValueError("La fecha de fin debe ser posterior a la fecha de inicio")
        return self


class BecaOtorgadaEstado(BaseModel):
    estotor: Literal["VIGENTE", "FINALIZADA", "REVOCADA", "SUSPENDIDA"]


class PostulacionResumen(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    codpost: int
    estudiante: EstudianteResumen
    convocatoria: ConvocatoriaResumen


class BecaOtorgadaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    codotor: int
    fechotor: date
    fechiniotor: date
    fechfinotor: date
    estotor: str
    codpost: int
    postulacion: PostulacionResumen
    cantseguimientos: int = 0
    promedioseguimiento: float | None = None  # lo calcula la función f2 de la BD


class SeguimientoBecaCreate(BaseModel):
    fechsegb: date
    promsegb: Decimal = Field(ge=0, le=20, max_digits=4, decimal_places=2)
    cumsegb: bool
    obssegb: str | None = None
    codperresp: int = Field(gt=0)


class SeguimientoBecaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    codsegb: int
    fechsegb: date
    promsegb: float
    cumsegb: bool
    obssegb: str | None
    codotor: int
    responsable: PersonalResumen
