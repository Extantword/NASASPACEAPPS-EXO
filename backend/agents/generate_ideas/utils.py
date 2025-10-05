import os
import random
from datetime import datetime
from cloud.cloud_constants import api_keys
from generate_ideas.generate_ideas import human, models_dict

import pytz

from generate_ideas.LLM_response import obtener_respuesta


def human_variations():
    '''Toma el contexto humano y le añade contexto sobre la hora'''

    print(f"current time: {colombia_now()}")

    human_hour_context = 'Redact the following prompt with your own words: "' + human +  f' First, keep in mind that the current time is sunday {colombia_now()}, so we just have that quantity of time to create, train and test the ML model'

    human_variations = [obtener_respuesta('groq', "", human_hour_context,  models_dict['groq'][0]) for _ in range(5)]

    return human_variations

def colombia_now():
    # Define the time zone for Colombia (e.g., America/Bogota)
    colombia_timezone = pytz.timezone('America/Bogota')

    # Get the current UTC time
    utc_now = datetime.utcnow()

    # Localize the UTC time to the Colombia time zone
    colombia_now = pytz.utc.localize(utc_now).astimezone(colombia_timezone).strftime('%Y-%m-%d %H:%M:%S %Z%z')
    return colombia_now

def get_random_key_for_service(service_name):
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

def get_random_service_key():
        """Return (service, key) for one random API key."""
        # flatten into a list of (service, key)
        all_pairs = [(service, key) for service, keys in api_keys.items() for key in keys]
        if not all_pairs:
            raise ValueError("No API keys loaded.")
        api_key = random.choice(all_pairs)
        service, key = api_key

        if service == "groq":
            os.environ["GROQ_API_KEY"] = key
        if service == "sambanova":
            os.environ["SAMBANOVA_API_KEY"] = key
        if service == "cerebras":
            os.environ["CEREBRAS_API_KEY"] = key
        if service == "googleaistudio":
            os.environ["GOOGLE_API_KEY"] = key

        return api_key

def elegir_modelo_aleatorio(models_dict):
        proveedor_elegido = random.choice(list(models_dict.keys()))

        modelos_del_proveedor = models_dict[proveedor_elegido]

        modelo_elegido = random.choice(modelos_del_proveedor)

        return proveedor_elegido, modelo_elegido

