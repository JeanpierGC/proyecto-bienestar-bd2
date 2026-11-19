from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.schemas.common import texto
from app.schemas.estudiante import Dni

CORREOMAX = 100


class PersonalCreate(BaseModel):
    nomper: texto(50)
    apeper: texto(50)
    dniper: Dni
    corrper: EmailStr
    cargoper: texto(50)
    codserv: int = Field(gt=0)

    @field_validator("corrper")
    @classmethod
    def correonoexcedelongitud(cls, correo: str) -> str:
        if len(correo) > CORREOMAX:
            raise ValueError(f"El correo no puede superar {CORREOMAX} caracteres")
        return correo


class ServicioResumen(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    codserv: int
    nomserv: str


class PersonalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    codper: int
    nomper: str
    apeper: str
    dniper: str
    corrper: str
    cargoper: str
    codserv: int
    servicio: ServicioResumen
