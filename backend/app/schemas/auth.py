from datetime import date

from pydantic import BaseModel, Field, model_validator


class LoginIn(BaseModel):
    nomusu: str = Field(min_length=1, max_length=30)
    clausu: str = Field(min_length=1, max_length=100)


class SesionOut(BaseModel):
    token: str
    codusu: int
    nomusu: str
    rolusu: str
    codest: int | None
    nombre: str
    horas: int


class UsuarioActual(BaseModel):
    """Datos que viajan dentro del token y que usan los permisos."""

    codusu: int
    rolusu: str
    codest: int | None


class DatosEstudiante(BaseModel):
    codest: int
    dniest: str
    correst: str
    cicest: int
    fnacest: date
    edad: int | None
    direst: str | None
    escuela: str
    facultad: str


class PerfilOut(BaseModel):
    nomusu: str
    rolusu: str
    nombre: str
    estudiante: DatosEstudiante | None


class CambioClave(BaseModel):
    actual: str = Field(min_length=1, max_length=100)
    nueva: str = Field(min_length=6, max_length=100)

    @model_validator(mode="after")
    def distinta(self):
        if self.actual == self.nueva:
            raise ValueError("La nueva contraseña debe ser distinta de la actual")
        return self
