from pydantic import BaseModel


class BecaOtorgadaPorConvocatoria(BaseModel):
    """Fila de la vista v02."""

    convocatoria: str
    beca: str
    cantotorgadas: int


class CuposConvocatoria(BaseModel):
    """Fila de la vista v06."""

    convocatoria: str
    cupos: int
    cantpostulaciones: int
    cantaprobadas: int


class RankingBeca(BaseModel):
    """Fila del procedimiento p07."""

    beca: str
    cantpostulaciones: int
    anio: int
