from datetime import date

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Convocatoria(Base):
    __tablename__ = "Convocatoria"

    codconv: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nomconv: Mapped[str] = mapped_column(String(100))
    perioconv: Mapped[str] = mapped_column(String(10))
    fechinconv: Mapped[date]
    fechfinconv: Mapped[date]
    cupconv: Mapped[int]
    estconv: Mapped[str] = mapped_column(String(15), default="ABIERTA")
    codbeca: Mapped[int] = mapped_column(ForeignKey("Beca.codbeca"))

    beca: Mapped["Beca"] = relationship(lazy="joined")
