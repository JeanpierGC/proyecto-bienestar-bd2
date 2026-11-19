from app.core.config import getsettings
from app.core.exceptions import ConflictError, NotFoundError
from app.core.seguridad import CredencialesError, creartoken, hashearclave, verificarclave
from app.models.usuario import Usuario
from app.repositories.usuariorepository import UsuarioRepository
from app.schemas.auth import CambioClave, DatosEstudiante, LoginIn, PerfilOut, SesionOut


class AuthService:
    def __init__(self, usuarios: UsuarioRepository) -> None:
        self.usuarios = usuarios

    def login(self, datos: LoginIn) -> SesionOut:
        usuario = self.usuarios.getbynombre(datos.nomusu.strip())
        # Un solo mensaje para usuario inexistente, clave mala o usuario inactivo:
        # no se le dice a quien prueba cuál de las tres fue.
        if usuario is None or usuario.estusu != "ACTIVO" or not verificarclave(datos.clausu, usuario.clausu):
            raise CredencialesError("Usuario o contraseña incorrectos")
        return self.sesion(usuario)

    def sesion(self, usuario: Usuario) -> SesionOut:
        token = creartoken({"codusu": usuario.codusu, "rolusu": usuario.rolusu, "codest": usuario.codest})
        return SesionOut(
            token=token, codusu=usuario.codusu, nomusu=usuario.nomusu, rolusu=usuario.rolusu,
            codest=usuario.codest, nombre=self.nombre(usuario), horas=getsettings().tokenhoras,
        )

    def nombre(self, usuario: Usuario) -> str:
        if usuario.estudiante is None:
            return "Administrador"
        return f"{usuario.estudiante.apeest}, {usuario.estudiante.nomest}"

    def perfil(self, codusu: int) -> PerfilOut:
        usuario = self.buscar(codusu)
        estudiante = usuario.estudiante
        datos = None
        if estudiante is not None:
            datos = DatosEstudiante(
                codest=estudiante.codest, dniest=estudiante.dniest, correst=estudiante.correst,
                cicest=estudiante.cicest, fnacest=estudiante.fnacest, edad=self.usuarios.edad(estudiante.codest),
                direst=estudiante.direst, escuela=estudiante.escuela.nomesc,
                facultad=estudiante.escuela.facultad.nomfac,
            )
        return PerfilOut(nomusu=usuario.nomusu, rolusu=usuario.rolusu, nombre=self.nombre(usuario), estudiante=datos)

    def cambiarclave(self, codusu: int, datos: CambioClave) -> None:
        usuario = self.buscar(codusu)
        if not verificarclave(datos.actual, usuario.clausu):
            raise ConflictError("La contraseña actual no es correcta")
        usuario.clausu = hashearclave(datos.nueva)
        self.usuarios.update(usuario)

    def buscar(self, codusu: int) -> Usuario:
        usuario = self.usuarios.getbyid(codusu)
        if usuario is None:
            raise NotFoundError("El usuario no existe")
        return usuario
