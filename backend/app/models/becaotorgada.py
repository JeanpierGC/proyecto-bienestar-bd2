from datetime import date
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class SeguimientoBeca(Base):
    __tablename__ = "SeguimientoBeca"

    codsegb: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fechsegb: Mapped[date]
    promsegb: Mapped[Decimal] = mapped_column(Numeric(4, 2))
    cumsegb: Mapped[bool]
    obssegb: Mapped[str | None] = mapped_column(Text)
    codotor: Mapped[int] = mapped_column(ForeignKey("BecaOtorgada.codotor"))
    codperresp: Mapped[int] = mapped_column(ForeignKey("Personal.codper"))

    responsable: Mapped["Personal"] = relationship(lazy="joined")


class BecaOtorgada(Base):
    __tablename__ = "BecaOtorgada"

    codotor: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fechotor: Mapped[date]
    fechiniotor: Mapped[date]
    fechfinotor: Mapped[date]
    estotor: Mapped[str] = mapped_column(String(12), default="VIGENTE")
    codpost: Mapped[int] = mapped_column(ForeignKey("Postulacion.codpost"), unique=True)

    postulacion: Mapped["Postulacion"] = relationship(lazy="joined", back_populates="otorgada")
    seguimientos: Mapped[list["SeguimientoBeca"]] = relationship(
        lazy="selectin", order_by="SeguimientoBeca.fechsegb.desc()"
    )
