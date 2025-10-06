'''DEPENDENCIAS'''


import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_sambanova import ChatSambaNovaCloud
from langchain_core.prompts import ChatPromptTemplate
from langchain_cerebras import ChatCerebras
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI # Added import
from datetime import datetime
from cloud.cloud_constants import models_dict, api_keys
import pytz
import random
import time

from ideas_orchestator.LLM_response import human_variations, obtener_respuesta
from ideas_orchestator.common import elegir_modelo_aleatorio
from ideas_orchestator.utils import get_random_service_key
from intercept_prints import *
from intercept_prints.intercept_prints import intercept_prints, procesar_print



'''API-KEYS'''

'''
api_keys = {
   "groq": os.environ["groq"],
   "sambanova": os.environ["sambanova"],
   "cerebras": os.environ["cerebras"],
   "googlaistudio": os.environ["googleaistudio"]
}
'''


'''MODELS'''

with open("SYSTEM.TXT", "r", encoding="utf-8") as f:
    system = f.read()

with open("HUMAN.TXT", "r", encoding="utf-8") as f:
    human = f.read()

with open("PROMPT_JUICIO.TXT", "r", encoding="utf-8") as f:
    prompt_juicio = f.read()


load_dotenv()

# ✅ Example
service, key = get_random_service_key()
print(f"Selected service: {service}\nAPI key: {key}")


# --- Nueva Función: Árbol de Búsqueda de Ideas ---

def arbol_busqueda_ideas(models_dict, system, X, Y):
    """
    Realiza un árbol de búsqueda para generar y refinar ideas de IA.

    Args:
        models_dict (dict): Diccionario con los modelos de IA disponibles.
        system (str): El prompt de sistema.
        human (str): El prompt humano inicial.
        X (int): Número de ideas iniciales a generar (ramas del árbol).
        Y (int): Número de refinamientos por cada idea.
    """
    print("*"*20)
    print("INICIANDO PROCESO DE ÁRBOL DE BÚSQUEDA DE IDEAS")
    print("*"*20 + "\n")

    ideas_refinadas_finales = []

    # --- PASO 1: Generación de X ideas iniciales ---
    for i in range(X):
        print(f"\n--- [RAMA {i+1}/{X}] Iniciando generación de idea ---")
        # Esta parte se asume que funciona correctamente
        cloud, model = elegir_modelo_aleatorio(models_dict)
        print(f"Seleccionado para generar idea: {cloud}/{model}")

#AQUÍ SE RANDOMIZA EL HUMAN 
        
        idea_actual = obtener_respuesta(cloud, system, random.choice(human_variations()), model)
        print(f"\nIDEA INICIAL {i+1}:\n'{idea_actual}'\n")

        # Para simular el proceso sin ejecutar el modelo real:
        # idea_actual = f"Idea de ejemplo inicial N°{i+1}"
        # print(f"\nIDEA INICIAL {i+1}:\n'{idea_actual}'\n")


        # --- PASO 2: Refinamiento de cada idea Y veces ---
        for j in range(Y):
            print(f"--- [RAMA {i+1}/{X}] Refinamiento {j+1}/{Y} ---")
            cloud_ref, model_ref = elegir_modelo_aleatorio(models_dict)
            print(f"Seleccionado para refinar: {cloud_ref}/{model_ref}")

            prompt_refinamiento = f"""
            Toma la siguiente idea y mejórala. Hazla más innovadora, más específica sobre el MVP
            y con más potencial para convertirse en un modelo SOTA (State-Of-The-Art).
            No te limites a repetir, debes añadir valor y evolucionar el concepto.

            IDEA A REFINAR:
            ---
            {idea_actual}
            ---   
            """
            idea_actual = obtener_respuesta(cloud_ref, system, prompt_refinamiento, model_ref)

            # Simulación del refinamiento:
            # idea_actual += f" (refinada {j+1} vez)"
            print(f"\nIDEA REFINADA {j+1}:\n'{idea_actual}'\n")

        ideas_refinadas_finales.append(idea_actual)
        print(f"--- [RAMA {i+1}/{X}] Fin de la rama. La idea final ha sido guardada. ---\n")

    # --- PASO 3: Juicio y análisis final de todas las ideas refinadas ---
    print("\n" + "*"*20)
    print("INICIANDO FASE DE JUICIO FINAL")
    print("Todas las ideas han sido generadas y refinadas.")
    print("*"*20 + "\n")

    # Juntamos todas las ideas para el prompt final
    ideas_para_juzgar = ""
    for idx, idea in enumerate(ideas_refinadas_finales):
        # CORRECCIÓN: Usar llaves sencillas para que la f-string inserte los valores.
        ideas_para_juzgar += f"--- IDEA {idx+1} ---\n{idea}\n\n"

    # CORRECCIÓN: Usar llaves sencillas para que la f-string inserte las variables
    # X y ideas_para_juzgar en la cadena de texto.


    print("Seleccionando un modelo aleatorio para el juicio final...")
    cloud_juez, model_juez = "googleaistudio", "gemini-2.5-pro" #elegir_modelo_aleatorio(models_dict)
    print(f"El JUEZ será: {cloud_juez}/{model_juez}")



    # Formatear el prompt_juicio con los valores correctos
    prompt_juicio_formatted = prompt_juicio.format(X=X, ideas_to_evaluate=ideas_para_juzgar)
    analisis_final = obtener_respuesta(cloud_juez, system, prompt_juicio_formatted, model_juez)

    print("\n" + "="*20)
    print("VEREDICTO FINAL DEL JUEZ")
    print("="*20)
    print(analisis_final)

    return analisis_final

#@intercept_prints(procesar_print)
def proceso_de_metajuicio(models_dict, system, X, Y, N_JUICIOS):
    """
    Ejecuta el proceso de árbol de búsqueda N veces y luego realiza un
    meta-juicio sobre los veredictos para obtener una conclusión de mayor calidad.

    Args:
        models_dict (dict): Diccionario con los modelos de IA disponibles.
        system (str): El prompt de sistema.
        human (str): El prompt humano inicial.
        X (int): Número de ideas iniciales por cada ejecución.
        Y (int): Número de refinamientos por cada idea.
        N_JUICIOS (int): Número de veces que se ejecutará el proceso completo.
    """
    print("\n" + "#"*40)
    print("### INICIANDO PROCESO DE META-JUICIO ###")
    print(f"### Se ejecutarán {N_JUICIOS} procesos de juicio completos. ###")
    print("#"*40 + "\n")

    lista_de_veredictos = []

    # --- PASO 1: Ejecutar el proceso N veces y recoger los veredictos ---
    for n in range(N_JUICIOS):
        print(f"\n--- [META-PROCESO {n+1}/{N_JUICIOS}] ---")
        veredicto_individual = arbol_busqueda_ideas(models_dict, system, X, Y)
        lista_de_veredictos.append(veredicto_individual)
        print(f"--- [FIN DEL META-PROCESO {n+1}/{N_JUICIOS}] ---\n")

    # --- PASO 2: Realizar el meta-juicio final ---
    print("\n" + "#"*40)
    print("### INICIANDO FASE DE META-JUICIO FINAL ###")
    print("Todos los veredictos individuales han sido generados.")
    print("#"*40 + "\n")

    # Juntamos todos los veredictos para el prompt final
    veredictos_para_juzgar = ""
    for idx, veredicto in enumerate(lista_de_veredictos):
        veredictos_para_juzgar += f"--- VEREDICTO DEL JUEZ {idx+1} ---\n{veredicto}\n\n"

    prompt_metajuicio = f"""
    Eres un estratega experto y supervisor de un panel de jueces de IA.
    Tu tarea es analizar los siguientes {N_JUICIOS} veredictos emitidos por diferentes jueces de IA sobre un conjunto de ideas para el NASA Space Apps Challenge.
    Cada juez ha analizado las mismas ideas subyacentes, pero puede haber llegado a conclusiones diferentes.

    Tu objetivo es sintetizar estos análisis para emitir una recomendación final y definitiva. No te limites a elegir un veredicto; en su lugar:
    1.  **Encuentra el Consenso**: Identifica qué ideas son consistentemente elogiadas en múltiples veredictos.
    2.  **Evalúa los Argumentos**: Determina qué juez presenta los argumentos más sólidos, lógicos y alineados con los criterios de innovación, viabilidad y potencial.
    3.  **Resuelve Contradicciones**: Si los jueces no están de acuerdo, analiza sus razonamientos y decide cuál es más convincente.
    4.  **Emite el Meta-Veredicto**: Proporciona un veredicto final que resuma los hallazgos y declare cuál es la idea ganadora definitiva, explicando por qué, basándote en la síntesis de los análisis proporcionados.

    Aquí están los veredictos a analizar:
    {veredictos_para_juzgar}
    """

    print("Seleccionando un modelo aleatorio para el META-JUICIO FINAL...")
    cloud_juez, model_juez = "googleaistudio", "gemini-2.5-pro" # elegir_modelo_aleatorio(models_dict)
    print(f"El META-JUEZ será: {cloud_juez}/{model_juez}")

    # Llamada final para obtener el meta-veredicto
    meta_veredicto_final = obtener_respuesta(cloud_juez, system, prompt_metajuicio, model_juez)

    print("\n" + "!"*20)
    print("!!! META-VEREDICTO FINAL !!!")
    print("!"*20)
    print(meta_veredicto_final)

    return meta_veredicto_final

    # --- Ejecución del Proceso ---
    # Supongamos que estas funciones y variables ya existen
    # def elegir_modelo_aleatorio(models_dict): ...
    # def obtener_respuesta(cloud, system, human, model): ...
    # models_dict = {...}
    # system = "..."
    # human = "..."


