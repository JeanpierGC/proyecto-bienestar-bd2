from sqlalchemy import CHAR, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Servicio(Base):
    __tablename__ = "Servicio"

    codserv: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nomserv: Mapped[str] = mapped_column(String(100), unique=True)
    descserv: Mapped[str | None] = mapped_column(Text)


class Personal(Base):
    __tablename__ = "Personal"

    codper: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nomper: Mapped[str] = mapped_column(String(50))
    apeper: Mapped[str] = mapped_column(String(50))
    dniper: Mapped[str] = mapped_column(CHAR(8), unique=True)
    corrper: Mapped[str] = mapped_column(String(100), unique=True)
    cargoper: Mapped[str] = mapped_column(String(50))
    codserv: Mapped[int] = mapped_column(ForeignKey("Servicio.codserv"))

    servicio: Mapped["Servicio"] = relationship(lazy="joined")
