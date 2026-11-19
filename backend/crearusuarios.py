"""Crea los usuarios del sistema (idempotente). Ejecutar desde la carpeta backend:

    python crearusuarios.py

- Administrador: usuario `admin`, contraseña `admin123`.
- Un usuario por estudiante: usuario = su DNI, contraseña inicial = su DNI.
Cambia estas contraseñas antes de usar el sistema fuera de las pruebas.
"""

from sqlalchemy import select

from app.core.database import SessionLocal
from app.core.seguridad import hashearclave
from app.models import Estudiante, Usuario
from app.repositories.usuariorepository import SQLAlchemyUsuarioRepository


def crear(repositorio, nomusu: str, clave: str, rolusu: str, codest: int | None) -> bool:
    if repositorio.getbynombre(nomusu):
        return False
    repositorio.add(Usuario(nomusu=nomusu, clausu=hashearclave(clave), rolusu=rolusu, codest=codest))
    return True


def main() -> None:
    with SessionLocal() as sesion:
        repositorio = SQLAlchemyUsuarioRepository(sesion)
        nuevos = int(crear(repositorio, "admin", "admin123", "ADMIN", None))
        for estudiante in sesion.scalars(select(Estudiante)).unique():
            nuevos += int(crear(repositorio, estudiante.dniest, estudiante.dniest, "ESTUDIANTE", estudiante.codest))
        print(f"usuarios creados: {nuevos}")


if __name__ == "__main__":
    main()
