from datetime import date

from sqlalchemy import CHAR, CheckConstraint, ForeignKey, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Estudiante(Base):
    __tablename__ = "Estudiante"
    __table_args__ = (CheckConstraint("cicest between 1 and 14"),)

    codest: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nomest: Mapped[str] = mapped_column(String(50))
    apeest: Mapped[str] = mapped_column(String(50))
    dniest: Mapped[str] = mapped_column(CHAR(8), unique=True)
    correst: Mapped[str] = mapped_column(String(100), unique=True)
    cicest: Mapped[int] = mapped_column(SmallInteger)
    fnacest: Mapped[date]
    direst: Mapped[str | None] = mapped_column(String(150))
    codesc: Mapped[int] = mapped_column(ForeignKey("Escuela.codesc"))

    escuela: Mapped["Escuela"] = relationship(back_populates="estudiantes", lazy="joined")
