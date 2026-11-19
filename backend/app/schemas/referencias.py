"""Datos mínimos de otras entidades, para mostrarlas dentro de postulaciones y becas otorgadas."""

from pydantic import BaseModel, ConfigDict

from app.schemas.beca import BecaResumen


class EstudianteResumen(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    codest: int
    nomest: str
    apeest: str
    dniest: str


class PersonalResumen(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    codper: int
    nomper: str
    apeper: str
    cargoper: str


class ConvocatoriaResumen(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    codconv: int
    nomconv: str
    perioconv: str
    estconv: str
    beca: BecaResumen
