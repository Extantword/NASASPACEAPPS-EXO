import os
import random
import sys
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_experimental.tools import PythonREPLTool

# Importar desde el archivo de herramientas final y estable
from llm_tools import (
    GetLabeledExoplanetDatasetTool,
    GetStarLightCurveTool,
    ListConfirmedExoplanetHostsTool,
    ListStarsByMissionTool
)

# --- PROMPT MEJORADO CON INSTRUCCIONES DE MANEJO DE ERRORES ---
# CÓDIGO CORREGIDO
SYSTEM_PROMPT = """Eres un agente de IA que debe seguir reglas muy estrictas.

Tienes acceso a las siguientes herramientas:
{tools}

Tu ciclo de trabajo es: Thought -> Action -> Observation.

**REGLAS CRÍTICAS:**
1.  **Thought:** Describe tu plan para el siguiente paso.
2.  **Action:** Responde con un único bloque de código JSON con una de las siguientes acciones: {tool_names}.
3.  Después de recibir una `Observation` de una herramienta, tu siguiente respuesta DEBE empezar INMEDIATAMENTE con `Thought:` o con `Final Answer:`.
4.  **REGLA FINAL:** Cuando hayas completado TODAS las tareas solicitadas por el usuario y verificado tu trabajo, tu respuesta final NO debe ser un JSON. Debe empezar directamente con la frase `Final Answer:` seguida de tu resumen completo.

EJEMPLO DE RESPUESTA FINAL CORRECTA:
Final Answer: He descargado exitosamente la curva de luz para la estrella X y he verificado que el archivo CSV contiene 1500 puntos de datos. La tarea ha sido completada.
EJEMPLO DE FLUJO CORRECTO:
...
Observation: [resultado de la herramienta]
Thought: La herramienta funcionó. Ahora debo hacer el siguiente paso, que es X.
Action:
```json
{{
  "action": "herramienta_X",
  "action_input": {{}}
}}
```

EJEMPLO DE FLUJO INCORRECTO:
...
Observation: [resultado de la herramienta]
¡Genial! La herramienta funcionó. Ahora voy a pensar qué hacer.  <-- ¡ESTO ESTÁ PROHIBIDO!
Thought: Ahora debo hacer X.
Action:
...
"""

def create_resilient_agent_executor():
    """Crea y configura un agente de IA que no se detiene ante errores."""
    
    try:
        llm = ChatGroq(model_name="deepseek-r1-distill-llama-70b", temperature=0.3)
    except Exception as e:
        print(f"🚨 Error al inicializar el modelo de Groq: {e}")
        sys.exit(1) # Salir si no podemos crear el modelo

    tools = [
        PythonREPLTool(),
        ListConfirmedExoplanetHostsTool(),
        GetStarLightCurveTool(),
        ListStarsByMissionTool(),
        GetLabeledExoplanetDatasetTool()
    ]

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", "{input}"),
        ("ai", "{agent_scratchpad}"),
    ])

    agent = create_structured_chat_agent(llm, tools, prompt)

    # --- CAMBIO CLAVE: HABILITAR EL MANEJO DE ERRORES ---
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        # Esto evita que el programa se caiga. El error se pasa al LLM como una observación.
        handle_parsing_errors=True,
        max_iterations=25
    )
    
    return agent_executor

def run_ML_Engineer(prompt_to_llm_engineer):
    """
    Función principal para configurar el entorno y ejecutar el agente resiliente.
    """
    os.environ["GROQ_API_KEY"] = random.choice(["PONER AQUÍ API-KEY"
             ])
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("🚨 Error: La variable de entorno GROQ_API_KEY no está configurada.")
        print("   Por favor, ejecute 'export GROQ_API_KEY=su_clave_aqui' en su terminal.")
        return

    print("🤖 Bot Científico de Datos (v5 - Final y Resiliente) está listo!")
    print("-" * 75)

    agent_executor = create_resilient_agent_executor()
    
    try:
        print(f"Usuario: {prompt_to_llm_engineer}\n")
        response = agent_executor.invoke({"input": prompt_to_llm_engineer})
        print("\n" + "="*75)
        print(f"Respuesta Final del Bot:\n{response['output']}")
        print("="*75)
    except Exception as e:
        # Este bloque ahora solo se activará si hay un error fundamental en el propio AgentExecutor
        print(f"\n🚨 Ocurrió un error crítico irrecuperable en el agente: {e}")

if __name__ == '__main__':
    # El prompt del usuario puede ser tan complejo como necesites.
    # El agente seguirá el plan paso a paso.
    user_prompt = """
**Rol:** Eres un Ingeniero Senior de Machine Learning especializado en arquitecturas de Deep Learning para análisis de series temporales y astronomía. Tu misión es implementar y validar un prototipo del innovador modelo "Pulsar", una arquitectura de IA físicamente informada para el descubrimiento de exoplanetas.

**Objetivo del Proyecto:** Construir un "modelo fundacional" para curvas de luz estelar utilizando aprendizaje auto-supervisado (Self-Supervised Learning - SSL). Este modelo debe aprender la estructura intrínseca y la física subyacente de la variabilidad estelar para luego ser utilizado en la detección de tránsitos de exoplanetas como anomalías.

**Filosofía Central:** No estamos entrenando un simple clasificador. Estamos enseñando a una máquina a "entender la música de las estrellas para encontrar los ritmos rotos". El núcleo de este proyecto es la tarea pretexto auto-supervisada llamada "Phase Cycle Consistency" (PCC).

---

### **PLAN DE EJECUCIÓN DETALLADO**

Sigue estos pasos de manera secuencial. Documenta cada paso con código, logs y visualizaciones.

#### **Paso 1: Configuración del Entorno y Adquisición de Datos**

1.  **Entorno:** Prepara un entorno de Python con las siguientes librerías principales: `PyTorch` (o TensorFlow), `NumPy`, `Pandas`, `Matplotlib`, `Scikit-learn`, `tqdm` y `lightkurve` (para acceder a datos de misiones como Kepler/TESS).
2.  **Adquisición de Datos:**
    *   Utiliza la librería `lightkurve` para descargar un conjunto de datos de curvas de luz del telescopio espacial TESS (o Kepler). Para este prototipo, enfócate en un conjunto manejable (ej. 10,000-20,000 curvas de luz de un solo sector de TESS).
    *   **No necesitas etiquetas en esta fase.** Descarga las curvas de luz pre-procesadas (ej. flujo PDCSAP). El objetivo es aprender de datos "crudos" (unlabeled data).
3.  **Pre-procesamiento:**
    *   **Normalización:** Normaliza cada curva de luz. Una técnica robusta es la estandarización (restar la media y dividir por la desviación estándar) o la normalización por mediana/MAD para ser resistente a outliers.     
    *   **Limpieza:** Elimina valores `NaN` y aplica un filtro de savitzky-golay o una mediana móvil para suavizar el ruido de alta frecuencia sin eliminar las señales de tránsito.
    *   **Segmentación:** Divide las curvas de luz largas en segmentos de longitud fija (ej. 2048 o 4096 puntos de datos). Esto crea nuestro conjunto de datos de entrenamiento para la fase auto-supervisada.

#### **Paso 2: Diseño de la Arquitectura del Modelo "Pulsar" (Encoder Híbrido)**

Implementa un encoder que combine lo mejor de las CNNs y los Transformers para capturar características locales y dependencias temporales a largo plazo.

1.  **Capa Convolucional (Extractor de Características Locales):**
    *   Inicia con una serie de bloques convolucionales 1D (`Conv1D`, `BatchNorm`, `ReLU`, `MaxPool`).
    *   El objetivo de esta capa es identificar formas y patrones locales, como la forma de "V" o "U" de un tránsito potencial, independientemente de su posición.
2.  **Capa Transformer (Contextualizador Temporal):**
    *   La salida de la capa CNN (un conjunto de vectores de características) se alimenta a un encoder Transformer estándar.
    *   Este Transformer aprenderá las relaciones temporales y la periodicidad en la curva de luz. Debe incluir codificación posicional (positional encoding) para mantener la información de la secuencia.
3.  **Salida del Encoder:** El encoder tomará un segmento de curva de luz como entrada y producirá un vector de embedding de dimensionalidad fija (ej. 256 o 512), que es una representación comprimida y rica en información de la curva de luz.

#### **Paso 3: Pre-entrenamiento Auto-Supervisado con "Phase Cycle Consistency" (PCC)**

Esta es la fase más crítica e innovadora.

1.  **Tarea Pretexto (PCC):**
    *   Para cada segmento de curva de luz en un batch:
        a. **Plegado (Folding):** Pliega la curva de luz sobre un **período de prueba aleatorio `P`**. Esto convierte la serie temporal en una representación de fase.
        b. **Aumentación de Datos (Phase-Shuffle):** Divide la curva de luz plegada en `N` bins (ej. `N=8`). Baraja aleatoriamente el orden de estos bins. Esta es la versión "corrupta" de la entrada.
        c. **Objetivo de Aprendizaje:** Alimenta la versión corrupta y plegada al encoder "Pulsar". La tarea del modelo es **predecir el orden original de los bins barajados**. Esto se puede formular como un problema de clasificación con `N!` clases (si N es pequeño) o, de forma más inteligente, como una tarea de regresión o clasificación para cada bin.
    *   **Función de Pérdida:** Utiliza `CrossEntropyLoss` si lo formulas como clasificación.
2.  **¿Por qué funciona PCC?:** Para resolver esta tarea, el modelo no puede simplemente memorizar patrones. Debe aprender implícitamente qué constituye un "ciclo coherente". Si el período de prueba `P` coincide con un período real en la señal (variabilidad estelar, rotación), la curva plegada será suave y estructurada. Si `P` es incorrecto, será ruidosa. El modelo debe aprender a reconocer la estructura inherente para poder "re-ordenar" los bins correctamente. En el proceso, aprende las leyes de Kepler de forma implícita.
3.  **Entrenamiento:** Entrena el encoder "Pulsar" en el gran conjunto de datos sin etiquetar usando la tarea PCC durante un número significativo de épocas, hasta que la pérdida de pre-entrenamiento converja. Guarda los pesos del encoder pre-entrenado.

#### **Paso 4: Evaluación del Modelo Fundacional**

Ahora que tenemos un encoder que "entiende" las curvas de luz, vamos a evaluar su poder.

**Método A: Fine-tuning con Pocas Etiquetas (Few-Shot Learning)**

1.  **Datos Etiquetados:** Obtén un conjunto de datos **pequeño y etiquetado** de curvas de luz (ej. del TESS Object of Interest - TOI catalog), con clases "Tránsito" y "No Tránsito".
2.  **Adaptación del Modelo:** Congela los pesos del encoder "Pulsar" pre-entrenado. Añade una pequeña cabeza de clasificación (un par de capas `Linear` con `ReLU` y una `Softmax` al final) sobre el encoder.
3.  **Fine-tuning:** Entrena **únicamente** la cabeza de clasificación con el pequeño conjunto de datos etiquetado. Como el encoder ya sabe extraer características potentes, este entrenamiento será muy rápido y eficiente.   

**Método B: Detección de Anomalías de Cero Disparos (Zero-Shot Anomaly Detection - ZAS-RD)**

1.  **Generación de Embeddings:** Pasa **todas** las curvas de luz (incluidas las que tienen tránsitos conocidos, pero sin usar sus etiquetas) a través del encoder "Pulsar" pre-entrenado para generar sus vectores de embedding.
2.  **Análisis del Espacio de Embeddings:**
    *   Visualiza el espacio de embeddings en 2D usando t-SNE o UMAP. La hipótesis es que las curvas de luz de estrellas "normales" y estables formarán un denso cúmulo, mientras que las curvas con anomalías (tránsitos, fulguraciones) se ubicarán en las afueras de este cúmulo.
    *   Utiliza un algoritmo de detección de anomalías (como `Isolation Forest` o `Local Outlier Factor`) sobre los embeddings para identificar las curvas de luz más atípicas.
3.  **Validación:** Comprueba si las anomalías mejor clasificadas por tu método corresponden a exoplanetas confirmados o candidatos conocidos.

#### **Paso 5: Generación de Reportes y Resultados**

Presenta un informe completo con las siguientes métricas y gráficos:

1.  **Curvas de Entrenamiento:**
    *   Gráfico de la pérdida de la tarea PCC durante el pre-entrenamiento auto-supervisado.
    *   Gráfico de la pérdida y la precisión durante el fine-tuning.
2.  **Métricas de Clasificación (para el Método A):**
    *   Matriz de confusión.
    *   Reporte de clasificación con Precisión, Recall y F1-Score para cada clase.
    *   Curva ROC y el valor del AUC.
3.  **Visualización del Espacio Latente (para el Método B):**
    *   Gráfico t-SNE/UMAP de los embeddings, coloreando puntos que se sabe que son planetas para verificar visualmente si se separan del cúmulo principal.
4.  **Análisis Cualitativo:**
    *   Muestra 3 ejemplos de tránsitos correctamente clasificados (curva de luz + predicción).
    *   Muestra 3 ejemplos de falsos positivos (curva de luz + predicción).
    *   Muestra 3 ejemplos de falsos negativos (curva de luz + predicción).
    *   Muestra las 5 curvas de luz con las puntuaciones de anomalía más altas del método ZAS-RD.

**Conclusión:** Finaliza con un breve resumen de los resultados, confirmando si el prototipo del modelo "Pulsar" demostró ser efectivo y si la filosofía del aprendizaje auto-supervisado es prometedora para esta tarea.       

### FIN DEL PROMPT ###"""
    run_ML_Engineer(user_prompt)