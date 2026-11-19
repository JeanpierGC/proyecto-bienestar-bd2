from datetime import date, time

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class SeguimientoCaso(Base):
    __tablename__ = "SeguimientoCaso"

    codseg: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fechseg: Mapped[date]
    descseg: Mapped[str] = mapped_column(Text)
    estseg: Mapped[str] = mapped_column(String(15), default="ABIERTO")
    fechprox: Mapped[date | None]
    codaten: Mapped[int] = mapped_column(ForeignKey("Atencion.codaten"))

    atencion: Mapped["Atencion"] = relationship(lazy="joined", back_populates="seguimientos")


class Atencion(Base):
    __tablename__ = "Atencion"

    codaten: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    resumaten: Mapped[str] = mapped_column(Text)
    recomaten: Mapped[str | None] = mapped_column(Text)
    nivelaten: Mapped[str] = mapped_column(String(10))
    reqseg: Mapped[bool] = mapped_column(default=False)
    codcita: Mapped[int] = mapped_column(ForeignKey("Cita.codcita"), unique=True)

    cita: Mapped["Cita"] = relationship(lazy="joined", back_populates="atencion")
    seguimientos: Mapped[list["SeguimientoCaso"]] = relationship(
        lazy="selectin", back_populates="atencion", order_by="SeguimientoCaso.fechseg.desc()"
    )


class Cita(Base):
    __tablename__ = "Cita"

    codcita: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fechcita: Mapped[date]
    horacita: Mapped[time]
    modcita: Mapped[str] = mapped_column(String(15))
    motcita: Mapped[str | None] = mapped_column(String(200))
    estcita: Mapped[str] = mapped_column(String(15), default="PROGRAMADA")
    codest: Mapped[int] = mapped_column(ForeignKey("Estudiante.codest"))
    codper: Mapped[int] = mapped_column(ForeignKey("Personal.codper"))

    estudiante: Mapped["Estudiante"] = relationship(lazy="joined")
    personal: Mapped["Personal"] = relationship(lazy="joined")
    atencion: Mapped["Atencion | None"] = relationship(
        lazy="selectin", uselist=False, back_populates="cita"
    )
