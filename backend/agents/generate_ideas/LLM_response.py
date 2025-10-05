import os
from langchain_cerebras import ChatCerebras
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_sambanova import ChatSambaNovaCloud
from langchain_core.prompts import ChatPromptTemplate

from generate_ideas.generate_ideas import get_random_key_for_service


def obtener_respuesta(cloud_service: str, system: str, human: str, modelo: str) -> str:
  get_random_key_for_service(cloud_service)
  
  if cloud_service == "groq":
    return obtener_respuesta_groq(system, human, modelo)
  if cloud_service == "sambanova":
    return obtener_respuesta_sambanova(system, human, modelo)
  if cloud_service == "cerebras":
    return obtener_respuesta_cerebras(system, human, modelo)
  if cloud_service == "googleaistudio":
    return obtener_respuesta_google(system, human, modelo)
  return "Servicio no soportado"

def obtener_respuesta_groq(system: str, human: str, modelo: str) -> str:
    """
    Obtiene una respuesta de un modelo de lenguaje de Groq dado un texto de entrada.

    Args:
        texto_entrada: El texto de entrada para el modelo de lenguaje.

    Returns:
        La respuesta generada por el modelo de lenguaje.
    """
    try:
        # Asegúrate de que la clave de API de Groq esté configurada como una variable de entorno.
        # Puedes obtener tu clave de API en: https://console.groq.com/keys
        if "GROQ_API_KEY" not in os.environ:
            print("Error: La variable de entorno GROQ_API_KEY no está configurada.")
            print("Por favor, establece tu clave de API de Groq.")
            return ""

        # Inicializa el modelo de chat de Groq.
        # Puedes elegir diferentes modelos, como "llama3-8b-8192" o "mixtral-8x7b-32768".
        chat = ChatGroq(model_name=modelo)

        prompt = ChatPromptTemplate.from_messages([
            ("system", system),
            ("human", human)
        ])

        # 3. Crea una cadena de LangChain
        chain = prompt | chat

        # 4. Invoca la cadena con tu pregunta
        respuesta = chain.invoke({})
        # La respuesta es un objeto, y el contenido real del mensaje está en el atributo 'content'.
        return respuesta.content

    except Exception as e:
        return f"Ha ocurrido un error: {e}"

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

    # 2. Inicializa el modelo de chat de Google
    # Por defecto, la API key se lee de la variable de entorno GOOGLE_API_KEY
    chat = ChatSambaNovaCloud(model=modelo, convert_system_message_to_human=True)

    # 3. Crea una plantilla de prompt
    # Nota: Algunos modelos de Gemini funcionan mejor con la instrucción del sistema
    # convertida a un mensaje humano, de ahí el parámetro en el paso anterior.
    prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        ("human", human)
    ])

    # 4. Crea una cadena de LangChain
    chain = prompt | chat

    # 5. Invoca la cadena. No se pasan argumentos aquí porque ya están en el prompt.
    respuesta = chain.invoke({})

    # 6. Devuelve el contenido de la respuesta
    return respuesta.content

def obtener_respuesta_cerebras(system: str, human: str, modelo: str) -> str:
    # 1. Inicializa el modelo de chat de Cerebras
    chat = ChatCerebras(model=modelo)

    # 2. Crea una plantilla de prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        ("human", human)
    ])

    # 3. Crea una cadena de LangChain
    chain = prompt | chat

    # 4. Invoca la cadena con tu pregunta
    respuesta = chain.invoke({})

    # 5. Imprime la respuesta
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

    # 2. Inicializa el modelo de chat de Google
    # Por defecto, la API key se lee de la variable de entorno GOOGLE_API_KEY
    chat = ChatGoogleGenerativeAI(model=modelo, convert_system_message_to_human=True)

    # 3. Crea una plantilla de prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        ("human", human)
    ])

    # 4. Crea una cadena de LangChain
    chain = prompt | chat

    # 5. Invoca la cadena. No se pasan argumentos aquí porque ya están en el prompt.
    respuesta = chain.invoke({})

    # 6. Devuelve el contenido de la respuesta
    return respuesta.content