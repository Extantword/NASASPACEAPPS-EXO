"""
Servicio unificado para operaciones con AWS S3.

Este módulo proporciona una clase S3Client que encapsula todas las operaciones
de subida y descarga de archivos con S3, así como funciones de alto nivel
para guardar logs automáticamente.

"""

import os
import logging
import tempfile
from datetime import datetime
from typing import Optional
import boto3
from botocore.exceptions import ClientError, NoCredentialsError


# Configuración del logging
logger = logging.getLogger(__name__)


class S3Client:
    """
    Cliente unificado para operaciones con AWS S3.
    
    Esta clase encapsula todas las operaciones de subida y descarga de archivos
    con S3, utilizando un cliente boto3 inicializado una sola vez.
    """
    
    def __init__(self, aws_access_key_id: Optional[str] = None, 
                 aws_secret_access_key: Optional[str] = None,
                 aws_region: str = 'us-east-1'):
        """
        Inicializa el cliente S3.
        
        Args:
            aws_access_key_id (str, opcional): AWS Access Key ID. Si no se proporciona,
                                             se obtiene de la variable de entorno.
            aws_secret_access_key (str, opcional): AWS Secret Access Key. Si no se proporciona,
                                                  se obtiene de la variable de entorno.
            aws_region (str): Región de AWS (por defecto: us-east-1)
        
        Raises:
            ValueError: Si las credenciales no están disponibles
        """
        # Obtener credenciales de parámetros o variables de entorno
        self.aws_access_key_id = aws_access_key_id or os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = aws_secret_access_key or os.getenv('AWS_SECRET_ACCESS_KEY')
        self.aws_region = aws_region or os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
        
        # Verificar que las credenciales estén disponibles
        if not self.aws_access_key_id or not self.aws_secret_access_key:
            error_msg = "Las credenciales de AWS no están configuradas. Asegúrate de que AWS_ACCESS_KEY_ID y AWS_SECRET_ACCESS_KEY estén en las variables de entorno."
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Inicializar cliente S3
        try:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.aws_region
            )
            logger.info(f"Cliente S3 inicializado correctamente para la región {self.aws_region}")
        except Exception as e:
            error_msg = f"Error al inicializar cliente S3: {str(e)}"
            logger.error(error_msg)
            raise ValueError(error_msg)
    
    def upload_file(self, file_name: str, bucket: str = "exo-nasa", object_name: Optional[str] = None) -> bool:
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
        
        # Verificar que el archivo local existe
        if not os.path.isfile(file_name):
            logger.error(f"Error: El archivo '{file_name}' no existe.")
            return False
        
        try:
            logger.info(f"Iniciando subida del archivo '{file_name}' al bucket '{bucket}' como '{object_name}'...")
            
            # Subir el archivo usando el cliente inicializado
            self.s3_client.upload_file(file_name, bucket, object_name)
            
            logger.info(f"¡Éxito! Archivo subido correctamente a s3://{bucket}/{object_name}")
            return True
            
        except FileNotFoundError:
            logger.error(f"Error: El archivo '{file_name}' no fue encontrado.")
            return False
            
        except NoCredentialsError:
            logger.error("Error: Credenciales de AWS no encontradas o inválidas.")
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
    
    def download_file(self, bucket: str, object_name: str, local_file_name: str) -> bool:
        """
        Descarga un archivo desde un bucket de AWS S3.
        
        Args:
            bucket (str): Nombre del bucket de S3 de origen
            object_name (str): Nombre y ruta del objeto en S3 a descargar
            local_file_name (str): Ruta local donde guardar el archivo descargado
        
        Returns:
            bool: True si la descarga fue exitosa, False en caso contrario
        """
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
            logger.info(f"Iniciando descarga del archivo 's3://{bucket}/{object_name}' a '{local_file_name}'...")
            
            # Descargar el archivo usando el cliente inicializado
            self.s3_client.download_file(bucket, object_name, local_file_name)
            
            logger.info(f"¡Éxito! Archivo descargado correctamente desde s3://{bucket}/{object_name} a {local_file_name}")
            return True
            
        except NoCredentialsError:
            logger.error("Error: Credenciales de AWS no encontradas o inválidas.")
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


def guardar_log(log_data: str, bucket: str = "exo-nasa", log_prefix: str = "logs/app") -> bool:
    """
    Función de alto nivel para guardar logs automáticamente en S3.
    
    Esta función crea un archivo temporal con el contenido del log,
    lo sube a S3 con un nombre único basado en timestamp, y luego
    elimina el archivo temporal.
    
    Args:
        log_data (str): Contenido del log a guardar
        bucket (str): Bucket de S3 donde guardar el log (por defecto: "exo-nasa")
        log_prefix (str): Prefijo para la ruta del log en S3 (por defecto: "logs/app")
    
    Returns:
        bool: True si el log se guardó exitosamente, False en caso contrario
    """
    # Importar el cliente configurado
    try:
        from app.config import s3_client
    except ImportError:
        logger.error("Error: No se pudo importar el cliente S3 desde app.config")
        return False
    
    # Generar nombre único para el archivo de log
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]  # microsegundos truncados
    log_filename = f"{log_prefix}/log_{timestamp}.txt"
    
    # Crear archivo temporal
    temp_file = None
    try:
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as tmp:
            # Escribir contenido del log con metadatos
            log_content = f"""# Log - NASA Space Apps Challenge - Exoplanet Explorer
# Timestamp: {datetime.now().isoformat()}
# Generated by: S3 Service Log Function

{log_data}

# End of log - {timestamp}
"""
            tmp.write(log_content)
            temp_file = tmp.name
        
        logger.info(f"Archivo temporal de log creado: {temp_file}")
        
        # Subir archivo a S3
        success = s3_client.upload_file(
            file_name=temp_file,
            bucket=bucket,
            object_name=log_filename
        )
        
        if success:
            logger.info(f"Log guardado exitosamente en s3://{bucket}/{log_filename}")
            return True
        else:
            logger.error("Error al subir el log a S3")
            return False
            
    except Exception as e:
        logger.error(f"Error al guardar log: {str(e)}")
        return False
        
    finally:
        # Eliminar archivo temporal
        if temp_file and os.path.exists(temp_file):
            try:
                os.unlink(temp_file)
                logger.debug(f"Archivo temporal eliminado: {temp_file}")
            except OSError as e:
                logger.warning(f"No se pudo eliminar archivo temporal {temp_file}: {str(e)}")