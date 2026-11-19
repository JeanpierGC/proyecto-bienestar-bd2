from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

EstadoSeguimiento = Literal["ABIERTO", "EN_PROCESO", "CERRADO"]


class SeguimientoCasoUpdate(BaseModel):
    fechseg: date
    descseg: str = Field(min_length=1)
    estseg: EstadoSeguimiento = "ABIERTO"
    fechprox: date | None = None

    @model_validator(mode="after")
    def validarproxima(self) -> "SeguimientoCasoUpdate":
        if self.fechprox is not None and self.fechprox < self.fechseg:
            raise ValueError("La próxima sesión no puede ser anterior al seguimiento")
        if self.estseg == "CERRADO" and self.fechprox is not None:
            raise ValueError("Un seguimiento cerrado no tiene próxima sesión")
        return self


class SeguimientoCasoCreate(SeguimientoCasoUpdate):
    codaten: int = Field(gt=0)


class SeguimientoCasoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    codseg: int
    fechseg: date
    descseg: str
    estseg: str
    fechprox: date | None
    codaten: int
