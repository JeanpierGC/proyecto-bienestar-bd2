from datetime import date
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, StringConstraints, field_validator

from app.schemas.common import texto
from app.schemas.escuela import EscuelaRead

Dni = Annotated[str, StringConstraints(strip_whitespace=True, pattern=r"^\d{8}$")]

CORREOMAX = 100


class EstudianteCreate(BaseModel):
    nomest: texto(50)
    apeest: texto(50)
    dniest: Dni
    correst: EmailStr
    cicest: int = Field(ge=1, le=14)
    fnacest: date
    direst: texto(150) | None = None
    codesc: int = Field(gt=0)

    @field_validator("correst")
    @classmethod
    def correonoexcedelongitud(cls, correo: str) -> str:
        if len(correo) > CORREOMAX:
            raise ValueError(f"El correo no puede superar {CORREOMAX} caracteres")
        return correo

    @field_validator("fnacest")
    @classmethod
    def fechanacimientonofutura(cls, fecha: date) -> date:
        if fecha > date.today():
            raise ValueError("La fecha de nacimiento no puede ser futura")
        return fecha


class EstudianteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    codest: int
    nomest: str
    apeest: str
    dniest: str
    correst: str
    cicest: int
    fnacest: date
    direst: str | None
    codesc: int
    escuela: EscuelaRead
