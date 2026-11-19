from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import texto


class RequisitoCreate(BaseModel):
    nomreq: texto(100)
    descreq: str | None = Field(default=None, max_length=255)


class RequisitoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    codreq: int
    nomreq: str
    descreq: str | None
