from datetime import date
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class RequisitoPostulacion(Base):
    """Documento que el estudiante presenta para un requisito de su postulación."""

    __tablename__ = "RequisitoPostulacion"

    codreq: Mapped[int] = mapped_column(ForeignKey("Requisito.codreq"), primary_key=True)
    codpost: Mapped[int] = mapped_column(ForeignKey("Postulacion.codpost"), primary_key=True)
    fechpres: Mapped[date]
    obsdoc: Mapped[str | None] = mapped_column(String(255))
    estdoc: Mapped[str] = mapped_column(String(12), default="PENDIENTE")


class Postulacion(Base):
    __tablename__ = "Postulacion"

    codpost: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fechpost: Mapped[date]
    prompost: Mapped[Decimal] = mapped_column(Numeric(4, 2))
    ingfampost: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    estpost: Mapped[str] = mapped_column(String(15), default="REGISTRADA")
    puntpost: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    fecheval: Mapped[date | None]
    obspost: Mapped[str | None] = mapped_column(Text)
    codest: Mapped[int] = mapped_column(ForeignKey("Estudiante.codest"))
    codconv: Mapped[int] = mapped_column(ForeignKey("Convocatoria.codconv"))
    codpereval: Mapped[int | None] = mapped_column(ForeignKey("Personal.codper"))

    estudiante: Mapped["Estudiante"] = relationship(lazy="joined")
    convocatoria: Mapped["Convocatoria"] = relationship(lazy="joined")
    evaluador: Mapped["Personal | None"] = relationship(lazy="joined")
    # Los documentos pertenecen a la postulación: se eliminan junto con ella.
    requisitos: Mapped[list["RequisitoPostulacion"]] = relationship(
        lazy="selectin", cascade="all, delete-orphan"
    )
    otorgada: Mapped["BecaOtorgada | None"] = relationship(
        lazy="selectin", uselist=False, back_populates="postulacion"
    )
