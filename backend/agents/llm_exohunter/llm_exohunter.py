import os
# --- 1. IMPORTAR EL CONSTRUCTOR Y HERRAMIENTAS ---
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_experimental.tools import PythonREPLTool

# Importar todas las herramientas personalizadas
'''from exoplanet_tools import (
    ListConfirmedExoplanetHostsTool,
    GetStarLightCurveTool,
    ListStarsByMissionTool,
    GetLabeledExoplanetDatasetTool
)'''

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


# --- 2. DEFINIR LA PLANTILLA DE PROMPT DETALLADA (Sin cambios) ---
SYSTEM_PROMPT = """Responde al usuario de la mejor manera posible. Tienes acceso a las siguientes herramientas:

{tools}

Para usar una herramienta, DEBES usar el siguiente formato EXACTO:

```
Thought: El usuario quiere que realice una acción. Debo elegir la herramienta correcta y proporcionar la entrada en el formato correcto.
Action:
```json
{{
  "action": "el_nombre_de_la_herramienta",
  "action_input": {{
    "nombre_del_argumento_1": "valor_1",
    "nombre_del_argumento_2": "valor_2"
  }}
}}
```
Observation: El resultado de la acción.
```

(este patrón de Thought/Action/Observation puede repetirse N veces)

Cuando tengas la respuesta final, DEBES usar el siguiente formato:
```
Thought: Ahora sé la respuesta final.
Final Answer: La respuesta final a la pregunta original del usuario.
```

**Instrucciones importantes:**
1.  La sección `Action` DEBE ser un bloque de código JSON válido.
2.  El campo `action_input` DEBE ser un objeto JSON, incluso si solo hay un argumento.
3.  El valor del campo `action` DEBE ser una de las siguientes opciones: **[{tool_names}]**.

**Ejemplo de uso de la herramienta `list_confirmed_exoplanet_hosts`:**

```
Thought: El usuario me pide una lista de 5 estrellas. Usaré la herramienta `list_confirmed_exoplanet_hosts`. El argumento se llama `max_results`.
Action:
```json
{{
  "action": "list_confirmed_exoplanet_hosts",
  "action_input": {{
    "max_results": 5
  }}
}}
``````
"""

def create_conversational_coding_chatbot():
    try:
        # Modelo actualizado para un mejor rendimiento potencial
        llm = ChatGroq(model_name="moonshotai/kimi-k2-instruct-0905", temperature=0)
    except Exception as e:
        print(f"Error initializing ChatGroq: {e}")
        return

    # --- Instanciamos TODAS las herramientas ---
    python_repl_tool = PythonREPLTool()
    list_hosts_tool = ListConfirmedExoplanetHostsTool()
    get_light_curve_tool = GetStarLightCurveTool()
    list_stars_mission_tool = ListStarsByMissionTool()
    get_ml_dataset_tool = GetLabeledExoplanetDatasetTool()

    tools = [
        python_repl_tool,
        list_hosts_tool,
        get_light_curve_tool,
        list_stars_mission_tool,
        get_ml_dataset_tool
    ]

    # --- 3. CREAR EL PROMPT (Sin cambios) ---
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("ai", "{agent_scratchpad}"),
    ])

    # --- 4. CREAR EL AGENTE Y EL EJECUTOR (Sin cambios) ---
    agent = create_structured_chat_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=15
    )

    chat_history_for_session = {}
    agent_with_chat_history = RunnableWithMessageHistory(
        agent_executor,
        lambda session_id: chat_history_for_session.setdefault(session_id, ChatMessageHistory()),
        input_messages_key="input",
        history_messages_key="chat_history",
    )

    print("🤖 Bot Científico de Datos (v2) está listo!")
    print("-" * 75)

    # Nuevo prompt de ejemplo para probar las nuevas herramientas
    session_id = "console_session"
    user_prompt = prompt_to_llm_engineer #"Descarga el dataset de Kepler para machine learning, cárgalo y dime cuántas características (columnas) tiene el archivo de features." #Ejemplo

    # Bucle principal (sin cambios)
    while True:
        try:
            if user_prompt:
                print(f"Tú: {user_prompt}")
            else:
                user_prompt = input("Tú: ")
            if user_prompt.lower() in ['exit', 'quit']:
                print("🤖 ¡Adiós!")
                break
            config = {"configurable": {"session_id": session_id}}
            response = agent_with_chat_history.invoke({"input": user_prompt}, config=config)
            print(f"Bot: {response['output']}")
            user_prompt = None
        except (KeyboardInterrupt, EOFError):
            print("\n🤖 ¡Sesión terminada!")
            break
        except Exception as e:
            print(f"\n🚨 Ocurrió un error inesperado: {e}")
            break

def run():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("🚨 Error: La variable de entorno GROQ_API_KEY no está configurada.")
    else:
        os.environ["GROQ_API_KEY"] = api_key
        # LangChain Tracing es opcional, se puede desactivar para mayor limpieza en la consola
        os.environ["LANGCHAIN_TRACING_V2"] = "false"
        os.environ["LANGCHAIN_API_KEY"] = ""
        create_conversational_coding_chatbot()}