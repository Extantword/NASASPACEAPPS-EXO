import os
from langchain_cerebras import ChatCerebras
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_sambanova import ChatSambaNovaCloud
from langchain_core.prompts import ChatPromptTemplate


from ideas_orchestator.common import colombia_now, get_random_service_key

from prompt.prompt import human, system
from cloud.cloud_constants import models_dict


human_list = []

def human_variations():
    '''Toma el contexto humano y le añade contexto sobre la hora'''
    global human_list

    print(f"current time: {colombia_now()}")

    human_hour_context = 'Redact the following prompt with your own words: "' + human +  f' First, keep in mind that the current time is sunday {colombia_now()}, so we just have that quantity of time to create, train and test the ML model'

    if not human_list:
        human_list = [obtener_respuesta('groq', "", human_hour_context,  models_dict['groq'][0]) for _ in range(5)]

    return human_list

def obtener_respuesta(cloud_service: str, system: str, human: str, modelo: str) -> str:
  
    get_random_service_key(cloud_service)

    # Escapar {error} en system y human para evitar KeyError en plantillas
    system_safe = system.replace('{error}', '{{error}}') if '{error}' in system else system
    human_safe = human.replace('{error}', '{{error}}') if '{error}' in human else human

    if cloud_service == "groq":
        result = obtener_respuesta_groq(system_safe, human_safe, modelo)
    elif cloud_service == "sambanova":
        result = obtener_respuesta_sambanova(system_safe, human_safe, modelo)
    elif cloud_service == "cerebras":
        result = obtener_respuesta_cerebras(system_safe, human_safe, modelo)
    elif cloud_service == "googleaistudio":
        result = obtener_respuesta_google(system_safe, human_safe, modelo)
    else:
        return "Servicio no soportado"

    # Si el resultado es un dict con 'error', devolver el mensaje de error
    if isinstance(result, dict) and 'error' in result:
        return f"[ERROR]: {result['error']}"
    return result

def obtener_respuesta_groq(system: str, human: str, modelo: str) -> str:
    """
    Obtiene una respuesta de un modelo de lenguaje de Groq dado un texto de entrada.

    Args:
        texto_entrada: El texto de entrada para el modelo de lenguaje.

    Returns:
        La respuesta generada por el modelo de lenguaje.
    """
    try:
        if "GROQ_API_KEY" not in os.environ:
            return "[ERROR]: Falta la variable de entorno GROQ_API_KEY"

        chat = ChatGroq(model_name=modelo)
        prompt = ChatPromptTemplate.from_messages([
            ("system", system),
            ("human", human)
        ])
        chain = prompt | chat
        respuesta = chain.invoke({"system": system, "human": human})
        return respuesta.content
    except Exception as e:
        return f"[ERROR]: {e}"

# Crear otras 3 funciones con las cuales podamos obtener una respuesta utilizando la libreria langchain de cada uno de los servicios cloud

def obtener_respuesta_sambanova(system: str, human: str, modelo: str) -> str:
    """
    Obtiene una respuesta de un modelo de Google AI Studio (Gemini) usando LangChain.

    Args:
        system: La instrucción o contexto para el modelo (rol del sistema).
        human: La pregunta o entrada del usuario.
        modelo: El nombre del modelo a utilizar (ej. "gemini-1.5-pro-latest").

    Returns:
        La respuesta generada por el modelo como una cadena de texto.
    """

    chat = ChatSambaNovaCloud(model=modelo, convert_system_message_to_human=True)
    prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        ("human", human)
    ])
    chain = prompt | chat
    respuesta = chain.invoke({"system": system, "human": human})
    return respuesta.content

def obtener_respuesta_cerebras(system: str, human: str, modelo: str) -> str:
    chat = ChatCerebras(model=modelo)
    prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        ("human", human)
    ])
    chain = prompt | chat
    respuesta = chain.invoke({"system": system, "human": human})
    return respuesta.content


def obtener_respuesta_google(system: str, human: str, modelo: str) -> str:
    """
    Obtiene una respuesta de un modelo de Google AI Studio (Gemini) usando LangChain.

    Args:
        system: La instrucción o contexto para el modelo (rol del sistema).
        human: La pregunta o entrada del usuario.
        modelo: El nombre del modelo a utilizar (ej. "gemini-1.5-pro-latest").

    Returns:
        La respuesta generada por el modelo como una cadena de texto.
    """

    chat = ChatGoogleGenerativeAI(model=modelo, convert_system_message_to_human=True)
    prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        ("human", human)
    ])
    chain = prompt | chat
    respuesta = chain.invoke({"system": system, "human": human})
    return respuesta.content