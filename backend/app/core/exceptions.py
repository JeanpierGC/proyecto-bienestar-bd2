class DomainError(Exception):
    """Error de regla de negocio. El mensaje se muestra tal cual al usuario."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class NotFoundError(DomainError):
    pass


class ConflictError(DomainError):
    pass
