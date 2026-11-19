from pydantic import BaseModel, ConfigDict

from app.schemas.common import texto


class FacultadCreate(BaseModel):
    nomfac: texto(100)


class FacultadRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    codfac: int
    nomfac: str
