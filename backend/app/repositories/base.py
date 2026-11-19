from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import Base

ModelT = TypeVar("ModelT", bound=Base)


class BaseRepository(ABC, Generic[ModelT]):
    """Contrato de acceso a datos del que dependen los services."""

    @abstractmethod
    def getbyid(self, entityid: int) -> ModelT | None: ...

    @abstractmethod
    def listall(self) -> list[ModelT]: ...

    @abstractmethod
    def count(self) -> int: ...

    @abstractmethod
    def add(self, entity: ModelT) -> ModelT: ...

    @abstractmethod
    def update(self, entity: ModelT) -> ModelT: ...

    @abstractmethod
    def delete(self, entity: ModelT) -> None: ...


class SQLAlchemyRepository(BaseRepository[ModelT]):
    """Implementación genérica del CRUD con SQLAlchemy."""

    model: type[ModelT]

    def __init__(self, session: Session) -> None:
        self.session = session

    def getbyid(self, entityid: int) -> ModelT | None:
        return self.session.get(self.model, entityid)

    def listall(self) -> list[ModelT]:
        return self.list(select(self.model))

    def count(self) -> int:
        return self.session.scalar(select(func.count()).select_from(self.model))

    def add(self, entity: ModelT) -> ModelT:
        self.session.add(entity)
        return self.save(entity)

    def update(self, entity: ModelT) -> ModelT:
        return self.save(entity)

    def delete(self, entity: ModelT) -> None:
        self.session.delete(entity)
        self.commit()

    def ordering(self) -> tuple[Any, ...]:
        """Columnas por las que se ordenan los listados. Se redefine en cada repositorio."""
        return ()

    def list(self, query) -> list[ModelT]:
        return list(self.session.scalars(query.order_by(*self.ordering())).unique())

    def first(self, query) -> ModelT | None:
        return self.session.scalars(query).unique().first()

    def save(self, entity: ModelT) -> ModelT:
        self.commit()
        self.session.refresh(entity)
        return entity

    def commit(self) -> None:
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
