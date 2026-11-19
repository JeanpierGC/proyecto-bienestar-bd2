from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import texto
from app.schemas.regla import ReglaRead
from app.schemas.requisito import RequisitoRead


class BecaCreate(BaseModel):
    nombeca: texto(100)
    tipobeca: texto(50)
    descbeca: str | None = Field(default=None, max_length=255)
    porcbeca: Decimal = Field(gt=0, le=100, max_digits=5, decimal_places=2)
    estbeca: Literal["ACTIVA", "INACTIVA"] = "ACTIVA"


class BecaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    codbeca: int
    nombeca: str
    tipobeca: str
    descbeca: str | None
    porcbeca: float
    estbeca: str
    reglas: list[ReglaRead]
    requisitos: list[RequisitoRead]


class BecaResumen(BaseModel):
    """Datos mínimos de una beca para mostrarla dentro de otras entidades."""

    model_config = ConfigDict(from_attributes=True)

    codbeca: int
    nombeca: str
    porcbeca: float


class BecaRequisitosUpdate(BaseModel):
    """Conjunto completo de requisitos que exige la beca."""

    codreq: list[int] = Field(default_factory=list)
