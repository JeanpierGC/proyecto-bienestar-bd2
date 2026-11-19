from app.repositories.escuelarepository import EscuelaRepository
from app.repositories.estudianterepository import EstudianteRepository
from app.repositories.facultadrepository import FacultadRepository
from app.schemas.resumen import CicloConteo, EscuelaConteo, ResumenAcademico

CICLOS = range(1, 15)
ULTIMOS = 5


class ResumenService:
    """Indicadores del módulo Académico para el panel principal."""

    def __init__(
        self,
        facultades: FacultadRepository,
        escuelas: EscuelaRepository,
        estudiantes: EstudianteRepository,
    ) -> None:
        self.facultades = facultades
        self.escuelas = escuelas
        self.estudiantes = estudiantes

    def obteneracademico(self) -> ResumenAcademico:
        return ResumenAcademico(
            totalfacultades=self.facultades.count(),
            totalescuelas=self.escuelas.count(),
            totalestudiantes=self.estudiantes.count(),
            ciclopromedio=self.estudiantes.averageciclo(),
            estudiantesporescuela=self.porescuela(),
            estudiantesporciclo=self.porciclo(),
            ultimosestudiantes=self.estudiantes.listlatest(ULTIMOS),
        )

    def porescuela(self) -> list[EscuelaConteo]:
        return [
            EscuelaConteo(codesc=codesc, nomesc=nomesc, nomfac=nomfac, total=total)
            for codesc, nomesc, nomfac, total in self.escuelas.countestudiantes()
        ]

    def porciclo(self) -> list[CicloConteo]:
        conteo = self.estudiantes.countbyciclo()
        return [CicloConteo(ciclo=ciclo, total=conteo.get(ciclo, 0)) for ciclo in CICLOS]
