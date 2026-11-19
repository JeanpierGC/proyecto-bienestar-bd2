from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Facultad(Base):
    __tablename__ = "Facultad"

    codfac: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nomfac: Mapped[str] = mapped_column(String(100), unique=True)

    escuelas: Mapped[list["Escuela"]] = relationship(back_populates="facultad")
