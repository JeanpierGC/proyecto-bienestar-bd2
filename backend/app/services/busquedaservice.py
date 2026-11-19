from app.repositories.busquedarepository import BusquedaRepository
from app.schemas.busqueda import EstudianteBusqueda


class BusquedaService:
    def __init__(self, busquedas: BusquedaRepository) -> None:
        self.busquedas = busquedas

    def estudiantes(self, apellido: str) -> list[EstudianteBusqueda]:
        apellido = apellido.strip()
        if not apellido:
            return []
        # p06 devuelve la fila completa de estudiante, leída por posición:
        # codest, nomest, apeest, dniest, correst, cicest, fnacest, direst, codesc
        return [
            EstudianteBusqueda(
                codest=fila[0], nomest=fila[1], apeest=fila[2], dniest=fila[3],
                cicest=fila[5], edad=self.busquedas.edad(fila[0]),
            )
            for fila in self.busquedas.porapellido(apellido)
        ]
