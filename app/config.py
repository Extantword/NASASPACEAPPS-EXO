"""
Configuración central de la aplicación NASA Space Apps Challenge - Exoplanet Explorer.

Este módulo centraliza toda la configuración de la aplicación, incluyendo:
- Carga de variables de entorno desde .env
- Inicialización del cliente S3
- Configuraciones generales de la aplicación
"""

import os
import logging
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Cargar variables de entorno desde .env al inicio de la aplicación
load_dotenv()

# Configuración del logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Configuración de la aplicación usando Pydantic."""
    
    app_name: str = "NASA Space Apps - Exoplanet Explorer"
    admin_email: str = "admin@exoplanet-explorer.com"
    items_per_user: int = 50
    
    # Configuración AWS S3
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_default_region: str = "us-east-1"
    s3_bucket_name: str = "exo-nasa"

    class Config:
        env_file = ".env"


# Instancia global de configuración
settings = Settings()

# Inicializar cliente S3 único para toda la aplicación
try:
    from app.services.s3_service import S3Client
    
    logger.info("Inicializando cliente S3...")
    s3_client = S3Client(
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        aws_region=os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    )
    logger.info("Cliente S3 inicializado exitosamente")
    
except Exception as e:
    logger.error(f"Error al inicializar cliente S3: {str(e)}")
    logger.warning("La aplicación continuará sin funcionalidad S3")
    s3_client = None