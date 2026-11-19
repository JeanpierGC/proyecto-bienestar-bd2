from typing import TypeVar

from pydantic import BaseModel

from app.core.exceptions import NotFoundError
from app.repositories.base import BaseRepository

ModelT = TypeVar("ModelT")


def obteneroerror(repository: BaseRepository[ModelT], entityid: int, entidad: str) -> ModelT:
    entity = repository.getbyid(entityid)
    if entity is None:
        raise NotFoundError(f"{entidad} con código {entityid} no existe")
    return entity


def asignarcampos(entity: object, datos: BaseModel) -> None:
    for campo, valor in datos.model_dump().items():
        setattr(entity, campo, valor)


def esotroregistro(encontrado: object | None, pk: str, entityid: int | None) -> bool:
    """Indica si un registro encontrado por un campo único pertenece a otra entidad."""
    return encontrado is not None and getattr(encontrado, pk) != entityid
