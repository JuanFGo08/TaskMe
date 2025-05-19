from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field, Field, AnyUrl, BeforeValidator, MySQLDsn
from typing import Literal, Annotated
from pydantic_core import MultiHostUrl


def parse_cors_origins(value: str) -> list[str] | str:
    """
    Parse the CORS origins from a string to a list of strings.
    """
    if isinstance(value, str) and not value.startswith("["):
        # If the value is a string and does not start with '[', treat it as a comma-separated list
        return [origin.strip() for origin in value.split(",") if origin.strip()]
    elif isinstance(value, list | str):
        return value
    raise ValueError(value)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        validate_assignment=True,
    )

    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_TIME: int = 3600 # 1 hour

    @computed_field
    @property
    def server_host(self) -> str:
        if self.ENVIRONMENT == "local":
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors_origins)
    ] = Field (default_factory=list)

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> MySQLDsn:
        return MultiHostUrl.build(
            scheme="mysql+pymysql",
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=self.DB_NAME,
        )
