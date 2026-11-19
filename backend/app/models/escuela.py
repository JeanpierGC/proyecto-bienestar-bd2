from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Escuela(Base):
    __tablename__ = "Escuela"
    __table_args__ = (UniqueConstraint("nomesc", "codfac"),)

    codesc: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nomesc: Mapped[str] = mapped_column(String(100))
    codfac: Mapped[int] = mapped_column(ForeignKey("Facultad.codfac"))

    facultad: Mapped["Facultad"] = relationship(back_populates="escuelas", lazy="joined")
    estudiantes: Mapped[list["Estudiante"]] = relationship(back_populates="escuela")
