"""Contraseñas y tokens de sesión con la biblioteca estándar de Python (sin dependencias nuevas)."""

import base64
import hashlib
import hmac
import json
import secrets
import time

from app.core.config import getsettings

ITERACIONES = 200_000


class CredencialesError(Exception):
    """Usuario o contraseña incorrectos (se responde 401)."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def hashearclave(clave: str) -> str:
    sal = secrets.token_bytes(16)
    resumen = hashlib.pbkdf2_hmac("sha256", clave.encode(), sal, ITERACIONES)
    return f"pbkdf2${ITERACIONES}${codificar(sal)}${codificar(resumen)}"


def verificarclave(clave: str, guardada: str) -> bool:
    try:
        _, iteraciones, sal, resumen = guardada.split("$")
        calculado = hashlib.pbkdf2_hmac("sha256", clave.encode(), decodificar(sal), int(iteraciones))
    except ValueError:
        return False
    return hmac.compare_digest(calculado, decodificar(resumen))


def creartoken(datos: dict) -> str:
    ajustes = getsettings()
    cuerpo = codificar(json.dumps({**datos, "exp": int(time.time()) + ajustes.tokenhoras * 3600}).encode())
    return f"{cuerpo}.{firmar(cuerpo)}"


def leertoken(token: str) -> dict | None:
    """Devuelve los datos del token, o None si fue alterado o ya venció."""
    try:
        cuerpo, firma = token.split(".")
        if not hmac.compare_digest(firma, firmar(cuerpo)):
            return None
        datos = json.loads(decodificar(cuerpo))
    except ValueError:
        return None
    return datos if datos.get("exp", 0) > time.time() else None


def firmar(cuerpo: str) -> str:
    clave = getsettings().secretkey.encode()
    return codificar(hmac.new(clave, cuerpo.encode(), hashlib.sha256).digest())


def codificar(datos: bytes) -> str:
    return base64.urlsafe_b64encode(datos).decode().rstrip("=")


def decodificar(texto: str) -> bytes:
    return base64.urlsafe_b64decode(texto + "=" * (-len(texto) % 4))
