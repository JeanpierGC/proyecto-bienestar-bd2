from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import texto
from app.schemas.facultad import FacultadRead


class EscuelaCreate(BaseModel):
    nomesc: texto(100)
    codfac: int = Field(gt=0)


class EscuelaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    codesc: int
    nomesc: str
    codfac: int
    facultad: FacultadRead
