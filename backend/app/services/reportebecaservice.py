from app.repositories.reportebecarepository import ReporteBecaRepository
from app.schemas.reportebeca import BecaOtorgadaPorConvocatoria, CuposConvocatoria, RankingBeca


class ReporteBecaService:
    """Convierte los resultados de las vistas y procedimientos en schemas de la API."""

    def __init__(self, reportes: ReporteBecaRepository) -> None:
        self.reportes = reportes

    def otorgadasconv(self) -> list[BecaOtorgadaPorConvocatoria]:
        return [
            BecaOtorgadaPorConvocatoria(convocatoria=convocatoria, beca=beca, cantotorgadas=cantidad)
            for convocatoria, beca, cantidad in self.reportes.otorgadasconv()
        ]

    def cuposconv(self) -> list[CuposConvocatoria]:
        return [
            CuposConvocatoria(
                convocatoria=convocatoria,
                cupos=cupos,
                cantpostulaciones=postulaciones,
                cantaprobadas=aprobadas,
            )
            for convocatoria, cupos, postulaciones, aprobadas in self.reportes.cuposconv()
        ]

    def rankingbecas(self, anio: int) -> list[RankingBeca]:
        return [
            RankingBeca(beca=beca, cantpostulaciones=cantidad, anio=aniopost)
            for beca, cantidad, aniopost in self.reportes.rankingbecas(anio)
        ]
