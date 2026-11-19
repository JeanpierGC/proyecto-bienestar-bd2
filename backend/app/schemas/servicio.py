from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import texto


class ServicioCreate(BaseModel):
    nomserv: texto(100)
    descserv: str | None = Field(default=None, max_length=255)


class ServicioRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    codserv: int
    nomserv: str
    descserv: str | None
