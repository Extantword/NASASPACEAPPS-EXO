# Base oficial de AWS Deep Learning Containers para entrenamiento PyTorch con GPU
FROM 763104351884.dkr.ecr.us-east-1.amazonaws.com/pytorch-training:2.6-gpu-py312-cu124-ubuntu22.04

# Instala SageMaker Training Toolkit para soporte de script mode y utilidades
RUN pip install --no-cache-dir sagemaker-training

# Directorio de código esperado
WORKDIR /opt/ml/code

# No copiar código ni requirements en la imagen — serán provistos en tiempo de job

# Define variable que SageMaker usa para saber qué script ejecutar
ENV SAGEMAKER_PROGRAM train.py

# ENTRYPOINT — este es el comando que ejecutará el script que inyectes
ENTRYPOINT ["python3", "/opt/ml/code/train.py"]
