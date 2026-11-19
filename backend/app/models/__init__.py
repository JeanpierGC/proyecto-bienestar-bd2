# Importar todos los modelos aquí permite que SQLAlchemy resuelva las relaciones.
from app.models.beca import Beca
from app.models.convocatoria import Convocatoria
from app.models.escuela import Escuela
from app.models.estudiante import Estudiante
from app.models.facultad import Facultad
from app.models.regla import Regla
from app.models.requisito import Requisito
from app.models.becaotorgada import BecaOtorgada, SeguimientoBeca
from app.models.personal import Personal, Servicio
from app.models.postulacion import Postulacion, RequisitoPostulacion
from app.models.cita import Atencion, Cita, SeguimientoCaso
from app.models.fichapsicologica import FichaPsicologica
from app.models.usuario import Usuario

__all__ = [
    "Usuario",
    "Atencion",
    "Cita",
    "SeguimientoCaso",
    "FichaPsicologica",
    "BecaOtorgada",
    "SeguimientoBeca",
    "Personal",
    "Servicio",
    "Postulacion",
    "RequisitoPostulacion",
    "Beca", "Convocatoria", "Escuela", "Estudiante", "Facultad", "Regla", "Requisito"]
