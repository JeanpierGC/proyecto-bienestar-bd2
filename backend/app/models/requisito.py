from sqlalchemy import Column, ForeignKey, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

# Tabla intermedia N:M entre Beca y Requisito (solo tiene las dos llaves).
requisitobeca = Table(
    "RequisitoBeca",
    Base.metadata,
    Column("codreq", ForeignKey("Requisito.codreq"), primary_key=True),
    Column("codbeca", ForeignKey("Beca.codbeca"), primary_key=True),
)


class Requisito(Base):
    __tablename__ = "Requisito"

    codreq: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nomreq: Mapped[str] = mapped_column(String(100), unique=True)
    descreq: Mapped[str | None] = mapped_column(Text)
