"""
Módulo para subir archivos a AWS S3 de forma segura.

Este módulo proporciona funcionalidad para subir archivos al bucket de S3 "exo-nasa"
utilizando credenciales cargadas desde variables de entorno para mayor seguridad.

Ejemplo de uso:
    from s3_uploader import upload_file_to_s3
    
    success = upload_file_to_s3("mi_archivo.txt", "exo-nasa")
    if success:
        print("Archivo subido exitosamente")
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


def upload_file_to_s3(file_name, bucket="exo-nasa", object_name=None):
    """
    Sube un archivo a un bucket de AWS S3.
    
    Args:
        file_name (str): Ruta local del archivo a subir
        bucket (str): Nombre del bucket de S3 de destino (por defecto: "exo-nasa")
        object_name (str, opcional): Nombre y ruta del objeto en S3. 
                                   Si no se especifica, usa file_name
    
    Returns:
        bool: True si la subida fue exitosa, False en caso contrario
    """
    
    # Si no se especifica object_name, usar el nombre del archivo
    if object_name is None:
        object_name = os.path.basename(file_name)
    
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
    
    # Verificar que el archivo local existe
    if not os.path.isfile(file_name):
        logger.error(f"Error: El archivo '{file_name}' no existe.")
        return False
    
    try:
        # Crear cliente de S3 con las credenciales cargadas
        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region
        )
        
        logger.info(f"Iniciando subida del archivo '{file_name}' al bucket '{bucket}' como '{object_name}'...")
        
        # Subir el archivo
        s3_client.upload_file(file_name, bucket, object_name)
        
        logger.info(f"¡Éxito! Archivo subido correctamente a s3://{bucket}/{object_name}")
        return True
        
    except FileNotFoundError:
        logger.error(f"Error: El archivo '{file_name}' no fue encontrado.")
        return False
        
    except NoCredentialsError:
        logger.error("Error: Credenciales de AWS no encontradas o inválidas.")
        logger.error("Verifica que AWS_ACCESS_KEY_ID y AWS_SECRET_ACCESS_KEY estén correctamente configuradas.")
        return False
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        
        if error_code == 'NoSuchBucket':
            logger.error(f"Error: El bucket '{bucket}' no existe.")
        elif error_code == 'AccessDenied':
            logger.error(f"Error: Acceso denegado al bucket '{bucket}'. Verifica los permisos.")
        elif error_code == 'InvalidAccessKeyId':
            logger.error("Error: AWS Access Key ID inválido.")
        elif error_code == 'SignatureDoesNotMatch':
            logger.error("Error: AWS Secret Access Key inválido.")
        else:
            logger.error(f"Error de AWS S3: {error_code} - {error_message}")
        
        return False
        
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        return False