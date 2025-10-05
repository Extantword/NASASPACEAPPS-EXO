"""
Módulo para descargar archivos desde AWS S3 de forma segura.

Este módulo proporciona funcionalidad para descargar archivos desde buckets de S3
utilizando credenciales cargadas desde variables de entorno para mayor seguridad.

"""

import os
import logging
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from dotenv import load_dotenv


# Configuración del logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def download_file_from_s3(bucket, object_name, local_file_name):
    """
    Descarga un archivo desde un bucket de AWS S3.
    
    Args:
        bucket (str): Nombre del bucket de S3 de origen
        object_name (str): Nombre y ruta del objeto en S3 a descargar
        local_file_name (str): Ruta local donde guardar el archivo descargado
    
    Returns:
        bool: True si la descarga fue exitosa, False en caso contrario
    """
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Obtener credenciales de AWS desde variables de entorno
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')  # Región por defecto
    
    # Verificar que las credenciales estén disponibles
    if not aws_access_key_id or not aws_secret_access_key:
        logger.error("Error: Las credenciales de AWS no están configuradas en las variables de entorno.")
        logger.error("Asegúrate de crear un archivo .env con AWS_ACCESS_KEY_ID y AWS_SECRET_ACCESS_KEY")
        return False
    
    # Crear el directorio local si no existe
    local_dir = os.path.dirname(local_file_name)
    if local_dir and not os.path.exists(local_dir):
        try:
            os.makedirs(local_dir, exist_ok=True)
            logger.info(f"Directorio creado: {local_dir}")
        except OSError as e:
            logger.error(f"Error al crear el directorio {local_dir}: {str(e)}")
            return False
    
    try:
        # Crear cliente de S3 con las credenciales cargadas
        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region
        )
        
        logger.info(f"Iniciando descarga del archivo 's3://{bucket}/{object_name}' a '{local_file_name}'...")
        
        # Descargar el archivo
        s3_client.download_file(bucket, object_name, local_file_name)
        
        logger.info(f"¡Éxito! Archivo descargado correctamente desde s3://{bucket}/{object_name} a {local_file_name}")
        return True
        
    except NoCredentialsError:
        logger.error("Error: Credenciales de AWS no encontradas o inválidas.")
        logger.error("Verifica que AWS_ACCESS_KEY_ID y AWS_SECRET_ACCESS_KEY estén correctamente configuradas.")
        return False
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        
        if error_code == '404' or error_code == 'NoSuchKey':
            logger.error(f"Error: El archivo '{object_name}' no se encuentra en el bucket '{bucket}'.")
        elif error_code == 'NoSuchBucket':
            logger.error(f"Error: El bucket '{bucket}' no existe.")
        elif error_code == 'AccessDenied':
            logger.error(f"Error: Acceso denegado al bucket '{bucket}' o al objeto '{object_name}'. Verifica los permisos.")
        elif error_code == 'InvalidAccessKeyId':
            logger.error("Error: AWS Access Key ID inválido.")
        elif error_code == 'SignatureDoesNotMatch':
            logger.error("Error: AWS Secret Access Key inválido.")
        else:
            logger.error(f"Error de AWS S3: {error_code} - {error_message}")
        
        return False
        
    except FileNotFoundError:
        logger.error(f"Error: No se pudo crear el archivo local '{local_file_name}'. Verifica la ruta.")
        return False
        
    except PermissionError:
        logger.error(f"Error: Sin permisos para escribir en '{local_file_name}'.")
        return False
        
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        return False