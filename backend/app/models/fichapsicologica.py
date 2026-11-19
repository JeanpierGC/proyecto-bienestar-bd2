from datetime import date

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class FichaPsicologica(Base):
    __tablename__ = "FichaPsicologica"

    codfic: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fechaper: Mapped[date]
    motfic: Mapped[str] = mapped_column(Text)
    antfic: Mapped[str | None] = mapped_column(Text)
    diagfic: Mapped[str | None] = mapped_column(Text)
    planfic: Mapped[str | None] = mapped_column(Text)
    estfic: Mapped[str] = mapped_column(String(10), default="ABIERTA")
    codest: Mapped[int] = mapped_column(ForeignKey("Estudiante.codest"))
    codperresp: Mapped[int] = mapped_column(ForeignKey("Personal.codper"))

    estudiante: Mapped["Estudiante"] = relationship(lazy="joined")
    responsable: Mapped["Personal"] = relationship(lazy="joined")
