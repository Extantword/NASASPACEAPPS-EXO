"""
Router de WebSockets para el sistema de chat de Exoplanet Explorer.

Este módulo define los endpoints WebSocket para el chat en tiempo real,
integrando el ConnectionManager existente con funcionalidad de chat.

Autor: NASA Space Apps Challenge Team
Fecha: Octubre 2025
"""

import json
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from datetime import datetime
from .connection_manager import manager

logger = logging.getLogger(__name__)

# Crear router para WebSockets
router = APIRouter(
    prefix="/ws",
    tags=["websockets"]
)

# Diccionario para mapear WebSockets a información de usuario del chat
chat_users = {}


@router.websocket("/chat/{client_id}")
async def websocket_chat_endpoint(websocket: WebSocket, client_id: str):
    """
    Endpoint principal para el chat WebSocket.
    
    Este endpoint maneja las conexiones de chat en tiempo real, permitiendo
    a los usuarios enviar y recibir mensajes instantáneamente.
    
    Args:
        websocket (WebSocket): La conexión WebSocket del cliente
        client_id (str): ID único del cliente/usuario
    """
    logger.info(f"Intento de conexión de chat desde cliente: {client_id}")
    
    try:
        # Conectar al cliente usando el gestor existente (grupo "chat")
        await manager.connect(websocket, "chat")
        
        # Almacenar información específica del chat
        chat_users[websocket] = {
            "client_id": client_id,
            "connected_at": datetime.now(),
            "message_count": 0
        }
        
        logger.info(f"Cliente {client_id} conectado al chat exitosamente")
        
        # Enviar mensaje de bienvenida
        welcome_message = {
            "type": "system",
            "message": f"🚀 ¡Bienvenido al chat de Exoplanet Explorer, {client_id}!",
            "timestamp": datetime.now().isoformat(),
            "sender": "Sistema",
            "clients_online": len(manager.active_connections.get("chat", []))
        }
        await manager.send_personal_message(welcome_message, websocket)
        
        # Notificar a otros usuarios sobre la nueva conexión
        if len(manager.active_connections.get("chat", [])) > 1:
            join_notification = {
                "type": "user_joined",
                "message": f"🌟 {client_id} se ha unido a la exploración",
                "timestamp": datetime.now().isoformat(),
                "sender": "Sistema",
                "clients_online": len(manager.active_connections.get("chat", []))
            }
            # Enviar a todos excepto al que se acaba de conectar
            for conn in manager.active_connections.get("chat", []):
                if conn != websocket:
                    await manager.send_personal_message(join_notification, conn)
        
        # Bucle principal para manejar mensajes
        while True:
            try:
                # Recibir mensaje del cliente
                data = await websocket.receive_text()
                logger.info(f"Mensaje recibido de {client_id}: {data}")
                
                # MODIFICACIÓN PARA DEBUGGING: Respuesta directa (eco) al cliente
                # Enviar confirmación inmediata solo al cliente que envió el mensaje
                await websocket.send_text("Servidor dice: Buenas noches, he recibido tu mensaje.")
                
                # ESTANDARIZACIÓN JSON: Decodificar mensaje entrante
                try:
                    # 1. Decodificar de string JSON a diccionario Python
                    message_data = json.loads(data)
                    # 2. Extraer el contenido del mensaje
                    message_content = message_data.get("message", "")
                except json.JSONDecodeError:
                    # Si no es JSON válido, tratarlo como texto plano
                    message_content = data
                    message_data = {"message": data, "type": "text"}
                
                # 3. Construir nuevo diccionario con estructura clara y consistente
                standardized_message = {
                    "sender": client_id,
                    "content": message_content,
                    "type": "message",
                    "timestamp": datetime.now().isoformat(),
                    "message_id": f"{client_id}_{chat_users.get(websocket, {}).get('message_count', 0) + 1}_{int(datetime.now().timestamp())}",
                    "clients_online": len(manager.active_connections.get("chat", []))
                }
                
                # Validar que el mensaje no esté vacío
                if not standardized_message["content"].strip():
                    error_message = {
                        "type": "error",
                        "message": "No puedes enviar mensajes vacíos",
                        "timestamp": datetime.now().isoformat(),
                        "sender": "Sistema"
                    }
                    await manager.send_personal_message(error_message, websocket)
                    continue
                
                # Filtrar palabras prohibidas y agregar contexto astronómico
                standardized_message["content"] = filter_message(standardized_message["content"])
                if any(keyword in standardized_message["content"].lower() for keyword in 
                       ["exoplanet", "kepler", "tess", "planeta", "estrella", "nasa"]):
                    standardized_message["category"] = "astronomy"
                    standardized_message["content"] += " 🌟"
                
                # Actualizar contador de mensajes del usuario
                user_info = chat_users.get(websocket, {})
                user_info["message_count"] = user_info.get("message_count", 0) + 1
                
                logger.info(f"Broadcasting mensaje estandarizado de {client_id} a todos los usuarios de chat")
                
                # 4. Codificar a string JSON antes del broadcast
                json_message = json.dumps(standardized_message)
                
                # Hacer broadcast del mensaje codificado
                await manager.broadcast(json_message, "chat")
                
            except WebSocketDisconnect:
                logger.info(f"Cliente {client_id} se desconectó del chat")
                break
            except Exception as e:
                logger.error(f"Error procesando mensaje de {client_id}: {str(e)}")
                # Enviar mensaje de error al cliente
                error_message = {
                    "type": "error",
                    "message": "Error procesando tu mensaje. Inténtalo de nuevo.",
                    "timestamp": datetime.now().isoformat(),
                    "sender": "Sistema"
                }
                await manager.send_personal_message(error_message, websocket)
                
    except Exception as e:
        logger.error(f"Error en conexión de chat para {client_id}: {str(e)}")
    
    finally:
        # Limpiar conexión
        await cleanup_chat_connection(websocket, client_id)


async def process_chat_message(websocket: WebSocket, client_id: str, message_data: dict):
    """
    Procesa un mensaje de chat y lo distribuye apropiadamente.
    
    Args:
        websocket (WebSocket): Conexión del remitente
        client_id (str): ID del cliente que envía el mensaje
        message_data (dict): Datos del mensaje
    """
    try:
        # Obtener información del usuario
        user_info = chat_users.get(websocket, {})
        user_info["message_count"] = user_info.get("message_count", 0) + 1
        
        # Crear estructura del mensaje para broadcast
        broadcast_message = {
            "type": message_data.get("type", "message"),
            "message": message_data.get("message", ""),
            "sender": client_id,
            "timestamp": datetime.now().isoformat(),
            "message_id": f"{client_id}_{user_info['message_count']}_{int(datetime.now().timestamp())}",
            "clients_online": len(manager.active_connections.get("chat", []))
        }
        
        # Validar que el mensaje no esté vacío
        if not broadcast_message["message"].strip():
            error_message = {
                "type": "error",
                "message": "No puedes enviar mensajes vacíos",
                "timestamp": datetime.now().isoformat(),
                "sender": "Sistema"
            }
            await manager.send_personal_message(error_message, websocket)
            return
        
        # Filtrar palabras prohibidas (opcional)
        broadcast_message["message"] = filter_message(broadcast_message["message"])
        
        # Agregar contexto de exoplanetas si es relevante
        if any(keyword in broadcast_message["message"].lower() for keyword in 
               ["exoplanet", "kepler", "tess", "planeta", "estrella", "nasa"]):
            broadcast_message["category"] = "astronomy"
            broadcast_message["message"] += " 🌟"
        
        logger.info(f"Broadcasting mensaje de {client_id} a todos los usuarios de chat")
        
        # Hacer broadcast del mensaje a todos los usuarios del chat
        await manager.broadcast(broadcast_message, "chat")
        
    except Exception as e:
        logger.error(f"Error procesando mensaje de chat: {str(e)}")
        raise


async def cleanup_chat_connection(websocket: WebSocket, client_id: str):
    """
    Limpia una conexión de chat cuando se desconecta.
    
    Args:
        websocket (WebSocket): Conexión a limpiar
        client_id (str): ID del cliente que se desconecta
    """
    try:
        # Desconectar del gestor
        manager.disconnect(websocket, "chat")
        
        # Remover de usuarios de chat
        if websocket in chat_users:
            del chat_users[websocket]
        
        # Notificar a otros usuarios sobre la desconexión
        if manager.active_connections.get("chat"):
            leave_notification = {
                "type": "user_left",
                "message": f"👋 {client_id} ha salido de la exploración",
                "timestamp": datetime.now().isoformat(),
                "sender": "Sistema",
                "clients_online": len(manager.active_connections.get("chat", []))
            }
            await manager.broadcast(leave_notification, "chat")
        
        logger.info(f"Conexión de chat limpiada para {client_id}")
        
    except Exception as e:
        logger.error(f"Error limpiando conexión de chat: {str(e)}")


def filter_message(message: str) -> str:
    """
    Filtra palabras inapropiadas del mensaje (implementación básica).
    
    Args:
        message (str): Mensaje original
        
    Returns:
        str: Mensaje filtrado
    """
    # Lista básica de palabras a filtrar (puedes expandir según necesidades)
    banned_words = ["spam", "hack", "virus"]
    
    filtered_message = message
    for word in banned_words:
        if word.lower() in filtered_message.lower():
            filtered_message = filtered_message.replace(word, "*" * len(word))
    
    return filtered_message


@router.websocket("/stats")
async def websocket_stats_endpoint(websocket: WebSocket):
    """
    Endpoint para estadísticas en tiempo real del chat.
    
    Proporciona información sobre usuarios conectados, mensajes, etc.
    """
    try:
        await manager.connect(websocket, "stats")
        logger.info("Cliente conectado a estadísticas de chat")
        
        while True:
            # Enviar estadísticas cada 5 segundos
            stats = {
                "type": "stats",
                "timestamp": datetime.now().isoformat(),
                "total_chat_users": len(manager.active_connections.get("chat", [])),
                "total_ml_users": len(manager.active_connections.get("ml_model", [])),
                "total_general_users": len(manager.active_connections.get("general", [])),
                "chat_users": [
                    {
                        "client_id": user_info.get("client_id"),
                        "connected_at": user_info.get("connected_at").isoformat() if user_info.get("connected_at") else None,
                        "message_count": user_info.get("message_count", 0)
                    }
                    for user_info in chat_users.values()
                ]
            }
            
            await manager.send_personal_message(stats, websocket)
            
            # Esperar 5 segundos antes del siguiente envío
            import asyncio
            await asyncio.sleep(5)
            
    except WebSocketDisconnect:
        logger.info("Cliente de estadísticas desconectado")
    except Exception as e:
        logger.error(f"Error en endpoint de estadísticas: {str(e)}")
    finally:
        manager.disconnect(websocket, "stats")