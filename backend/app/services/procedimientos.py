from app.core.exceptions import ConflictError, NotFoundError


def exigirmensaje(mensaje: str, esperado: str) -> None:
    """Los procedimientos de la BD responden con un texto en vez de lanzar errores.

    Si el texto no es el de éxito, se convierte en el error de negocio que corresponde.
    """
    if mensaje == esperado:
        return
    if "no existe" in mensaje:
        raise NotFoundError(mensaje)
    raise ConflictError(mensaje)
