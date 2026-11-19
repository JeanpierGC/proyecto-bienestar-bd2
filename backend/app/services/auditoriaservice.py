import re

from app.repositories.auditoriarepository import AuditoriaRepository
from app.schemas.auditoria import RegistroAuditoria


FECHADOBLE = re.compile(r"(\d{4}-\d\d-\d\d)-(\d{4}-\d\d-\d\d)")


def valor(texto: str | None, accion: str) -> str:
    """En las actualizaciones el trigger guarda 'antes-después'; aquí se muestra solo lo que cambió."""
    if texto is None or accion != "ACTUALIZACION":
        return str(texto)
    partes = FECHADOBLE.fullmatch(texto)
    antes, despues = partes.groups() if partes else (texto.split("-", 1) + [""])[:2]
    return antes if antes == despues else f"{antes} → {despues}"


class AuditoriaService:
    """Convierte las filas de control en registros legibles para la pantalla de auditoría."""

    def __init__(self, auditoria: AuditoriaRepository) -> None:
        self.auditoria = auditoria

    def postulaciones(self) -> list[RegistroAuditoria]:
        return [
            RegistroAuditoria(
                idctrl=idctrl, fecha=fecha, accion=accion, codigo=valor(codigo, accion),
                detalle=f"Estado {valor(estado, accion)} · promedio {valor(promedio, accion)} · estudiante {valor(estudiante, accion)} · convocatoria {valor(convocatoria, accion)}",
            )
            for idctrl, fecha, accion, codigo, estado, promedio, estudiante, convocatoria
            in self.auditoria.postulaciones()
        ]

    def otorgamientos(self) -> list[RegistroAuditoria]:
        return [
            RegistroAuditoria(
                idctrl=idctrl, fecha=fecha, accion=accion, codigo=valor(codigo, accion),
                detalle=f"Estado {valor(estado, accion)} · del {valor(inicio, accion)} al {valor(fin, accion)} · postulación {valor(postulacion, accion)}",
            )
            for idctrl, fecha, accion, codigo, estado, inicio, fin, postulacion
            in self.auditoria.otorgamientos()
        ]

    def citas(self) -> list[RegistroAuditoria]:
        return [
            RegistroAuditoria(
                idctrl=idctrl, fecha=fecha, accion=accion, codigo=valor(codigo, accion),
                detalle=f"{valor(fechacita, accion)} {valor(hora, accion)} · {valor(estado, accion)} · estudiante {valor(estudiante, accion)} · profesional {valor(profesional, accion)}",
            )
            for idctrl, fecha, accion, codigo, fechacita, hora, estado, estudiante, profesional
            in self.auditoria.citas()
        ]
