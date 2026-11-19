from decimal import Decimal

from sqlalchemy import Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.requisito import requisitobeca


class Beca(Base):
    __tablename__ = "Beca"

    codbeca: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombeca: Mapped[str] = mapped_column(String(100), unique=True)
    tipobeca: Mapped[str] = mapped_column(String(50))
    descbeca: Mapped[str | None] = mapped_column(Text)
    porcbeca: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    estbeca: Mapped[str] = mapped_column(String(10), default="ACTIVA")

    # Las reglas pertenecen a la beca: se eliminan junto con ella.
    reglas: Mapped[list["Regla"]] = relationship(
        lazy="selectin", cascade="all, delete-orphan", order_by="Regla.codreg"
    )
    requisitos: Mapped[list["Requisito"]] = relationship(
        secondary=requisitobeca, lazy="selectin", order_by="Requisito.nomreq"
    )
