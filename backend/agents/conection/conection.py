from ideas_orchestator.LLM_response import obtener_respuesta
from cloud.cloud_constants import models_dict
from ideas_orchestator.common import elegir_modelo_aleatorio, get_random_service_key
from prompt.prompt import system


def prompt_to_llm_engineer(final_conclusion):
    prompt_conection = f'''
    anteriormente se hizo un proceso de busqueda y analisis de nuevas ideas de arquitecturas para exoplanet hunting.

    con esto se llegó a las siguientes conclusiones:

    {final_conclusion}

    Ahora lo que debes hacer es crear un prompt para un LLM Agente ML Engineer que cree el modelo, lo entrene con los datos necesarios
    (que en este caso son solo datos de intensidad de luz/tiempo) y nos muestre los resultados por medio de metricas y
    graficos. Escribe el prompt entre ```
    '''

    cloud, model = elegir_modelo_aleatorio(models_dict)

    print(f"cloud: {cloud}")
    print(f"model: {model}")
    print("-"*10)

    key = get_random_service_key(cloud)

    prompt_to_llm_engineer = obtener_respuesta(cloud, system, prompt_conection, model).split("```")[1]

    return prompt_to_llm_engineer