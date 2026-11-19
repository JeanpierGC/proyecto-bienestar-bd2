from app.repositories.reportepostulacionrepository import ReportePostulacionRepository
from app.schemas.reportepostulacion import PostulacionesPorEstudiante, PromedioSeguimientoBeca


class ReportePostulacionService:
    """Convierte los resultados de las vistas en schemas de la API."""

    def __init__(self, reportes: ReportePostulacionRepository) -> None:
        self.reportes = reportes

    def porestudiante(self) -> list[PostulacionesPorEstudiante]:
        return [
            PostulacionesPorEstudiante(estudiante=estudiante, cantpostulaciones=cantidad, anio=anio)
            for estudiante, cantidad, anio in self.reportes.porestudiante()
        ]

    def promediosbeca(self) -> list[PromedioSeguimientoBeca]:
        return [
            PromedioSeguimientoBeca(beca=beca, promedio=promedio, cantseguimientos=cantidad)
            for beca, promedio, cantidad in self.reportes.promediosbeca()
        ]
