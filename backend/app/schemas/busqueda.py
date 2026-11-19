from pydantic import BaseModel


class EstudianteBusqueda(BaseModel):
    """Resultado del procedimiento p06 más la edad que calcula la función f3."""

    codest: int
    nomest: str
    apeest: str
    dniest: str
    cicest: int
    edad: int
