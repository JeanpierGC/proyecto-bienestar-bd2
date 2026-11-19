from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.referencias import ConvocatoriaResumen, EstudianteResumen, PersonalResumen

EstadoDocumento = Literal["PENDIENTE", "APROBADO", "OBSERVADO", "RECHAZADO"]


class PostulacionCreate(BaseModel):
    codest: int = Field(gt=0)
    codconv: int = Field(gt=0)
    prompost: Decimal = Field(ge=0, le=20, max_digits=4, decimal_places=2)
    ingfampost: Decimal = Field(ge=0, max_digits=10, decimal_places=2)


class PostulacionEvaluar(BaseModel):
    puntpost: Decimal = Field(ge=0, max_digits=5, decimal_places=2)
    estpost: Literal["EN_EVALUACION", "APROBADA", "RECHAZADA"]
    codpereval: int = Field(gt=0)


class OtorgadaResumen(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    codotor: int
    estotor: str


class PostulacionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    codpost: int
    fechpost: date
    prompost: float
    ingfampost: float
    estpost: str
    puntpost: float | None
    fecheval: date | None
    codest: int
    codconv: int
    estudiante: EstudianteResumen
    convocatoria: ConvocatoriaResumen
    evaluador: PersonalResumen | None
    otorgada: OtorgadaResumen | None
    mensajeestado: str | None = None  # lo calcula la función f4 de la BD


class ConteoPostulaciones(BaseModel):
    codest: int
    cantidad: int  # lo calcula la función f1 de la BD


class RequisitoPresentado(BaseModel):
    """Requisito que exige la beca y, si el estudiante ya lo presentó, el estado de su documento."""

    codreq: int
    nomreq: str
    fechpres: date | None = None
    estdoc: EstadoDocumento | None = None
    obsdoc: str | None = None


class RequisitoPresentadoUpdate(BaseModel):
    estdoc: EstadoDocumento = "PENDIENTE"
    obsdoc: str | None = Field(default=None, max_length=255)
