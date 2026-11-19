from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schemas.beca import BecaResumen
from app.schemas.common import texto


class ConvocatoriaCreate(BaseModel):
    nomconv: texto(100)
    perioconv: texto(10)
    fechinconv: date
    fechfinconv: date
    cupconv: int = Field(gt=0)
    estconv: Literal["ABIERTA", "CERRADA", "EN_EVALUACION"] = "ABIERTA"
    codbeca: int = Field(gt=0)

    @model_validator(mode="after")
    def validarfechas(self) -> "ConvocatoriaCreate":
        if self.fechfinconv < self.fechinconv:
            raise ValueError("La fecha de fin no puede ser anterior a la fecha de inicio")
        return self


class ConvocatoriaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    codconv: int
    nomconv: str
    perioconv: str
    fechinconv: date
    fechfinconv: date
    cupconv: int
    estconv: str
    codbeca: int
    beca: BecaResumen
    cuposdisponibles: int | None = None  # lo calcula la función f6 de la BD
