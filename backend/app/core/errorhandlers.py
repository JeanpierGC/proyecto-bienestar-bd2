from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import ConflictError, NotFoundError


def error(status_code: int, message: str) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"detail": message})


async def notfound(_: Request, exc: NotFoundError) -> JSONResponse:
    return error(status.HTTP_404_NOT_FOUND, exc.message)


async def conflict(_: Request, exc: ConflictError) -> JSONResponse:
    return error(status.HTTP_409_CONFLICT, exc.message)


async def integrity(_: Request, __: IntegrityError) -> JSONResponse:
    # Última defensa: la BD rechazó la operación (registro duplicado o en uso).
    return error(
        status.HTTP_409_CONFLICT,
        "La operación viola una restricción de la base de datos "
        "(registro duplicado o relacionado con otros datos).",
    )


def registerexceptionhandlers(app: FastAPI) -> None:
    app.add_exception_handler(NotFoundError, notfound)
    app.add_exception_handler(ConflictError, conflict)
    app.add_exception_handler(IntegrityError, integrity)
