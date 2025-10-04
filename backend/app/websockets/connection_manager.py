"""
WebSocket connection manager for handling client connections and broadcasts.
"""
from typing import Dict, List, Any
import asyncio
import json
from fastapi import WebSocket
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    """
    Manager for WebSocket connections.
    Handles connections, disconnections, and messages between clients and ML models.
    """
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {
            "general": [],  # General connections
            "ml_model": []  # ML model specific connections
        }
        
    async def connect(self, websocket: WebSocket, client_type: str = "general"):
        """
        Connect a new client to the appropriate connection group
        
        Args:
            websocket: The WebSocket connection
            client_type: Type of client (general or ml_model)
        """
        await websocket.accept()
        if client_type not in self.active_connections:
            self.active_connections[client_type] = []
            
        self.active_connections[client_type].append(websocket)
        logger.info(f"Client connected to {client_type} group. Total connections: {len(self.active_connections[client_type])}")
    
    def disconnect(self, websocket: WebSocket, client_type: str = "general"):
        """
        Disconnect a client
        
        Args:
            websocket: The WebSocket connection
            client_type: Type of client (general or ml_model)
        """
        if client_type in self.active_connections:
            try:
                self.active_connections[client_type].remove(websocket)
                logger.info(f"Client disconnected from {client_type} group. Remaining connections: {len(self.active_connections[client_type])}")
            except ValueError:
                logger.warning(f"Attempted to disconnect a client that wasn't in the {client_type} group")
    
    async def send_personal_message(self, message: Any, websocket: WebSocket):
        """
        Send a message to a specific client
        
        Args:
            message: Message to send
            websocket: Target WebSocket connection
        """
        if isinstance(message, dict) or isinstance(message, list):
            message = json.dumps(message)
        await websocket.send_text(message)
    
    async def broadcast(self, message: Any, client_type: str = "general"):
        """
        Broadcast a message to all connected clients of a specific type
        
        Args:
            message: Message to broadcast
            client_type: Type of clients to broadcast to
        """
        if client_type not in self.active_connections:
            logger.warning(f"Attempted to broadcast to non-existent group: {client_type}")
            return
            
        if isinstance(message, dict) or isinstance(message, list):
            message = json.dumps(message)
            
        disconnected = []
        for connection in self.active_connections[client_type]:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error sending message to client: {str(e)}")
                disconnected.append(connection)
        
        # Clean up disconnected clients
        for connection in disconnected:
            self.disconnect(connection, client_type)
    
    async def stream_ml_predictions(self, model_type: str, data_stream: asyncio.Queue, client_type: str = "ml_model"):
        """
        Stream ML model predictions to connected clients
        
        Args:
            model_type: Type of ML model being used
            data_stream: Queue with prediction data
            client_type: Type of clients to stream to
        """
        logger.info(f"Starting ML prediction stream for model: {model_type}")
        
        try:
            while True:
                # Get data from the stream queue
                data = await data_stream.get()
                
                # Check if we should terminate the stream
                if data is None or data == "STOP":
                    logger.info(f"Stopping ML prediction stream for model: {model_type}")
                    break
                
                # Add model type info to the data
                if isinstance(data, dict):
                    data["model_type"] = model_type
                    data["timestamp"] = str(asyncio.get_event_loop().time())
                
                # Broadcast to all connected clients
                await self.broadcast(data, client_type)
                
                # Mark task as done
                data_stream.task_done()
                
                # Small delay to prevent flooding
                await asyncio.sleep(0.01)
                
        except asyncio.CancelledError:
            logger.info(f"ML prediction stream for model {model_type} was cancelled")
        except Exception as e:
            logger.error(f"Error in ML prediction stream: {str(e)}")
    
    async def handle_ml_request(self, message: dict, websocket: WebSocket, model_service):
        """
        Handle ML request from a client and stream response
        
        Args:
            message: Request message
            websocket: Client WebSocket connection
            model_service: ML model service for processing
        """
        try:
            # Extract request data
            request_id = message.get("request_id", "unknown")
            model_type = message.get("model_type", "random_forest")
            features = message.get("features", {})
            
            logger.info(f"Processing ML request {request_id} for model {model_type}")
            
            # Create response stream queue
            response_queue = asyncio.Queue()
            
            # Start streaming task
            stream_task = asyncio.create_task(
                self.stream_ml_response(websocket, response_queue, request_id)
            )
            
            # Process with model service
            await model_service.process_streaming_request(
                features, model_type, response_queue
            )
            
            # Signal end of stream
            await response_queue.put({"status": "complete", "request_id": request_id})
            
            # Wait for streaming to complete
            await stream_task
            
        except Exception as e:
            logger.error(f"Error handling ML request: {str(e)}")
            await self.send_personal_message(
                {"error": str(e), "request_id": message.get("request_id")},
                websocket
            )
    
    async def stream_ml_response(self, websocket: WebSocket, response_queue: asyncio.Queue, request_id: str):
        """
        Stream ML model responses to a specific client
        
        Args:
            websocket: Client WebSocket connection
            response_queue: Queue with response data
            request_id: ID of the request being processed
        """
        try:
            while True:
                # Get response from the queue
                response = await response_queue.get()
                
                # Add request ID to the response
                if isinstance(response, dict):
                    response["request_id"] = request_id
                
                # Send to the client
                await self.send_personal_message(response, websocket)
                
                # Mark task as done
                response_queue.task_done()
                
                # Check if this is the end of the stream
                if isinstance(response, dict) and response.get("status") == "complete":
                    break
                    
                # Small delay to prevent flooding
                await asyncio.sleep(0.01)
                
        except asyncio.CancelledError:
            logger.info(f"ML response stream for request {request_id} was cancelled")
        except Exception as e:
            logger.error(f"Error in ML response stream: {str(e)}")


# Create a manager instance to be used across the app
manager = ConnectionManager()