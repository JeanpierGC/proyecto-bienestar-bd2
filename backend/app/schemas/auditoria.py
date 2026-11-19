from datetime import datetime

from pydantic import BaseModel


class RegistroAuditoria(BaseModel):
    """Fila de una tabla de control (ctrl_postu, ctrl_otor o ctrl_cita) que llenan los triggers."""

    idctrl: int
    accion: str
    fecha: datetime
    codigo: str | None
    detalle: str
