from typing import Annotated

from pydantic import StringConstraints


def texto(max_length: int) -> type[str]:
    """Texto obligatorio, sin espacios sobrantes y con longitud máxima."""
    return Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=max_length)
    ]
