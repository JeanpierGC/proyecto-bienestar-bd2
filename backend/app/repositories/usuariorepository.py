from abc import abstractmethod

from sqlalchemy import func, select

from app.models.usuario import Usuario
from app.repositories.base import BaseRepository, SQLAlchemyRepository


class UsuarioRepository(BaseRepository[Usuario]):
    @abstractmethod
    def getbynombre(self, nomusu: str) -> Usuario | None: ...

    @abstractmethod
    def edad(self, codest: int) -> int | None:
        """Edad del estudiante según la función f3."""


class SQLAlchemyUsuarioRepository(SQLAlchemyRepository[Usuario], UsuarioRepository):
    model = Usuario

    def getbynombre(self, nomusu: str) -> Usuario | None:
        return self.first(select(Usuario).where(Usuario.nomusu == nomusu))

    def edad(self, codest: int) -> int | None:
        return self.session.scalar(select(func.f3(codest)))

    def ordering(self):
        return (Usuario.nomusu,)
