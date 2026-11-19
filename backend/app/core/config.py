from functools import lru_cache
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración leída desde variables de entorno o el archivo .env."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    dbhost: str = "localhost"
    dbport: int = 3306
    dbuser: str = "root"
    dbpassword: str = ""
    dbname: str = "dbbecasbienestar"
    # Clave con la que se firman las sesiones: cámbiala en .env (SECRETKEY) antes de publicar el sistema.
    secretkey: str = "cambia-esta-clave-en-el-env"
    tokenhoras: int = 8

    @property
    def databaseurl(self) -> str:
        password = quote_plus(self.dbpassword)
        return (
            f"mysql+pymysql://{self.dbuser}:{password}"
            f"@{self.dbhost}:{self.dbport}/{self.dbname}?charset=utf8mb4"
        )


@lru_cache
def getsettings() -> Settings:
    return Settings()
