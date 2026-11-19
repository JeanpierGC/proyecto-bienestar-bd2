from app.repositories.reportebienestarrepository import ReporteBienestarRepository
from app.schemas.reportebienestar import CasoRiesgo, CitasPorProfesional


class ReporteBienestarService:
    """Convierte los resultados de las vistas en schemas de la API."""

    def __init__(self, reportes: ReporteBienestarRepository) -> None:
        self.reportes = reportes

    def citasprofesional(self) -> list[CitasPorProfesional]:
        return [
            CitasPorProfesional(profesional=profesional, servicio=servicio, cantcitas=cantidad)
            for profesional, servicio, cantidad in self.reportes.citasprofesional()
        ]

    def casosriesgo(self) -> list[CasoRiesgo]:
        return [
            CasoRiesgo(
                estudiante=estudiante, fechacita=fecha, nivel=nivel,
                estadoseguimiento=estado, proximafecha=proxima,
            )
            for estudiante, fecha, nivel, estado, proxima in self.reportes.casosriesgo()
        ]
