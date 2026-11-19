from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import texto

Operador = Literal[">=", "<=", ">", "<", "="]


class ReglaCreate(BaseModel):
    nomreg: texto(100)
    opreg: Operador
    valreg: Decimal = Field(max_digits=8, decimal_places=2)
    descreg: str | None = Field(default=None, max_length=255)
    codbeca: int = Field(gt=0)


class ReglaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    codreg: int
    nomreg: str
    opreg: str
    valreg: float
    descreg: str | None
    codbeca: int
