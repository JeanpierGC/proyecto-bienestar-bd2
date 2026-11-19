from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


def llamar(session: Session, sql: str, params: dict[str, Any]) -> list[tuple[Any, ...]]:
    """Ejecuta un procedimiento almacenado, confirma sus cambios y devuelve las filas que retorna."""
    try:
        filas = [tuple(fila) for fila in session.execute(text(sql), params)]
        session.commit()
    except Exception:
        session.rollback()
        raise
    # Los procedimientos cambian filas por fuera del ORM: se descarta lo que había en caché.
    session.expire_all()
    return filas


def llamarmensaje(session: Session, sql: str, params: dict[str, Any]) -> str:
    """Para los procedimientos que responden con una sola fila: el texto `mensaje`."""
    return llamar(session, sql, params)[0][0]
