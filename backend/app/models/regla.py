from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Regla(Base):
    """Condición de aplicación de una beca. Ej.: promedio >= 14."""

    __tablename__ = "Regla"

    codreg: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nomreg: Mapped[str] = mapped_column(String(100))
    opreg: Mapped[str] = mapped_column(String(2))
    valreg: Mapped[Decimal] = mapped_column(Numeric(8, 2))
    descreg: Mapped[str | None] = mapped_column(Text)
    codbeca: Mapped[int] = mapped_column(ForeignKey("Beca.codbeca"))
