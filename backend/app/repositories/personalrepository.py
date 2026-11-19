from abc import abstractmethod

from sqlalchemy import exists, select

from app.models.personal import Personal
from app.repositories.base import BaseRepository, SQLAlchemyRepository


class PersonalRepository(BaseRepository[Personal]):
    @abstractmethod
    def getbydni(self, dniper: str) -> Personal | None: ...

    @abstractmethod
    def getbycorreo(self, corrper: str) -> Personal | None: ...

    @abstractmethod
    def existsbyservicio(self, codserv: int) -> bool: ...


class SQLAlchemyPersonalRepository(SQLAlchemyRepository[Personal], PersonalRepository):
    model = Personal

    def getbydni(self, dniper: str) -> Personal | None:
        return self.first(select(Personal).where(Personal.dniper == dniper))

    def getbycorreo(self, corrper: str) -> Personal | None:
        return self.first(select(Personal).where(Personal.corrper == corrper))

    def existsbyservicio(self, codserv: int) -> bool:
        return self.session.scalar(select(exists().where(Personal.codserv == codserv)))

    def ordering(self):
        return (Personal.apeper, Personal.nomper)
