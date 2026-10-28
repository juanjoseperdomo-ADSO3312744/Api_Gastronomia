import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class JSettings(BaseSettings):
    """
    Configuración global de la aplicación cargada desde variables de entorno.
    """
    PROJECT_NAME: str = "API REST Gastronomia CGDSS"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"

    # Base de Datos MongoDB
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "bd_gastronomia_nosql"

    # Seguridad JWT
    SECRET_KEY: str = "clave_secreta_super_segura_para_jwt_gastronomia_sena_2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


@lru_cache()
def j_obtener_configuracion() -> JSettings:
    """
    Retorna la instancia de configuración con caché para evitar lecturas de disco repetidas.
    """
    return JSettings()


j_settings = j_obtener_configuracion()
