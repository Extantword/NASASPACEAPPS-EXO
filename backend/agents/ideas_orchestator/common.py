from datetime import datetime
import os
import random

import pytz
from cloud.cloud_constants import api_keys

def colombia_now():
    # Define the time zone for Colombia (e.g., America/Bogota)
    colombia_timezone = pytz.timezone('America/Bogota')

    # Get the current UTC time
    utc_now = datetime.utcnow()

    # Localize the UTC time to the Colombia time zone
    colombia_now = pytz.utc.localize(utc_now).astimezone(colombia_timezone).strftime('%Y-%m-%d %H:%M:%S %Z%z')
    return colombia_now

def get_random_service_key(service_name):
        """Return a random API key for the given service."""
        if service_name not in api_keys:
            raise ValueError(f"Servicio '{service_name}' no encontrado. Los servicios disponibles son: {list(api_keys.keys())}")

        keys_for_service = api_keys[service_name]
        if not keys_for_service:
            raise ValueError(f"No se encontraron API keys para el servicio '{service_name}'.")

        key = random.choice(keys_for_service)

        if service_name == "groq":
            os.environ["GROQ_API_KEY"] = key
        elif service_name == "sambanova":
            os.environ["SAMBANOVA_API_KEY"] = key
        elif service_name == "cerebras":
            os.environ["CEREBRAS_API_KEY"] = key
        elif service_name == "googleaistudio":
            os.environ["GOOGLE_API_KEY"] = key

        return service_name, key

def elegir_modelo_aleatorio(models_dict):
        proveedor_elegido = random.choice(list(models_dict.keys()))

        modelos_del_proveedor = models_dict[proveedor_elegido]

        modelo_elegido = random.choice(modelos_del_proveedor)

        return proveedor_elegido, modelo_elegido
