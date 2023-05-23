from pydantic import BaseSettings
from typing import Dict, Any
import logging

class Settings(BaseSettings):
    ANALYTICS_DB_HOST: str
    ANALYTICS_DB_PORT: int
    ANALYTICS_DB_DATABASE: str
    ANALYTICS_DB_USERNAME: str
    ANALYTICS_DB_PASSWORD: str
    DB_PRIMAVERA_HOST: str
    DB_PRIMAVERA_PORT: int
    DB_PRIMAVERA_USERNAME: str
    DB_PRIMAVERA_PASSWORD: str
    DB_PRIMAVERA_DBNAME: str
    SQL_PARAMS: Dict[str, Any] = {"proj_name": "MPS01"}
    GENERAL_PARAMS: Dict[str, Any] = {"ot": "OTTESTING01", "datadate": "2023-05-11"}
    VERSION: str = "1.0.0"
    TITLE: str = "Microservice weekly"
    DESCRIPTION: str = 'This microservice return data of weekly'
    OPENAPI_SCHEMA_URL: str = "https://tecnasic.aimacloud.app/assets/aima_logos/Logotipo-AIMA---negro.png"
    REDOC_URL: str = "/api/v1/weekly/documentation"
    ENVIRONMENT: str
    AUTH_URL: str
    IN_SERVER: bool = False
    MS_NAME: str
    SERVICE_ACRONYM: str
    LOG_LEVEL: str = 'INFO'  # Nivel de registro predeterminado


    def setup_logging(self):
        logging.basicConfig(
            format='%(asctime)s [%(levelname)s]: %(message)s',
            level=self.LOG_LEVEL,
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    class Config:
        env_file = ".env"

settings = Settings()
settings.setup_logging()
