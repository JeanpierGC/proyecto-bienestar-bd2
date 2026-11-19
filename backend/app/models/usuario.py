from sqlalchemy import CheckConstraint, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Usuario(Base):
    __tablename__ = "Usuario"
    __table_args__ = (
        CheckConstraint("rolusu in ('ADMIN','ESTUDIANTE')"),
        CheckConstraint("estusu in ('ACTIVO','INACTIVO')"),
    )

    codusu: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nomusu: Mapped[str] = mapped_column(String(30), unique=True)
    clausu: Mapped[str] = mapped_column(String(200))
    rolusu: Mapped[str] = mapped_column(String(12))
    estusu: Mapped[str] = mapped_column(String(10), default="ACTIVO")
    codest: Mapped[int | None] = mapped_column(ForeignKey("Estudiante.codest"), unique=True)

    estudiante: Mapped["Estudiante | None"] = relationship(lazy="joined")
