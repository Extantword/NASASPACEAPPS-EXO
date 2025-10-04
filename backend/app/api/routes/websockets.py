"""
WebSocket API routes for real-time ML model communication.
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
import logging
import json
import asyncio
from typing import Dict, Any, Optional

from app.websockets import manager
from app.services.ml_websocket_service import MLWebSocketService
from app.models.schemas import MLClassificationRequest

router = APIRouter()
logger = logging.getLogger(__name__)

# Create ML service instance
ml_service = MLWebSocketService()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """General WebSocket endpoint for all clients"""
    await manager.connect(websocket, "general")
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                message_type = message.get("type", "unknown")
                
                if message_type == "ping":
                    await manager.send_personal_message({"type": "pong"}, websocket)
                elif message_type == "ml_request":
                    # Handle ML model request separately
                    await handle_ml_request(websocket, message)
                else:
                    # Echo back the message as a default behavior
                    await manager.send_personal_message(
                        {"type": "echo", "content": message},
                        websocket
                    )
            except json.JSONDecodeError:
                await manager.send_personal_message(
                    {"type": "error", "message": "Invalid JSON format"},
                    websocket
                )
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")
                await manager.send_personal_message(
                    {"type": "error", "message": f"Error processing message: {str(e)}"},
                    websocket
                )
    except WebSocketDisconnect:
        manager.disconnect(websocket, "general")
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        manager.disconnect(websocket, "general")


@router.websocket("/ws/ml/{model_type}")
async def ml_websocket_endpoint(websocket: WebSocket, model_type: str):
    """ML-specific WebSocket endpoint for streaming model predictions"""
    if model_type not in ["random_forest", "neural_network"]:
        await websocket.close(code=1008, reason=f"Unsupported model type: {model_type}")
        return
        
    await manager.connect(websocket, "ml_model")
    try:
        # Send initial connection confirmation
        await manager.send_personal_message(
            {
                "type": "connection",
                "status": "connected",
                "model": model_type
            },
            websocket
        )
        
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                message_type = message.get("type", "unknown")
                
                if message_type == "ping":
                    await manager.send_personal_message({"type": "pong"}, websocket)
                elif message_type == "start_stream":
                    # Start streaming predictions from the ML model
                    await start_ml_stream(websocket, model_type, message)
                elif message_type == "stop_stream":
                    # Stop any active streams for this client
                    await stop_ml_stream(websocket, message)
                elif message_type == "classify":
                    # Process a single classification request
                    await handle_classification(websocket, model_type, message)
                else:
                    await manager.send_personal_message(
                        {"type": "error", "message": f"Unsupported message type: {message_type}"},
                        websocket
                    )
            except json.JSONDecodeError:
                await manager.send_personal_message(
                    {"type": "error", "message": "Invalid JSON format"},
                    websocket
                )
            except Exception as e:
                logger.error(f"Error processing ML message: {str(e)}")
                await manager.send_personal_message(
                    {"type": "error", "message": f"Error processing message: {str(e)}"},
                    websocket
                )
    except WebSocketDisconnect:
        manager.disconnect(websocket, "ml_model")
        await ml_service.stop_stream_for_client(websocket)
    except Exception as e:
        logger.error(f"ML WebSocket error: {str(e)}")
        manager.disconnect(websocket, "ml_model")
        await ml_service.stop_stream_for_client(websocket)


async def handle_ml_request(websocket: WebSocket, message: Dict[str, Any]):
    """Handle a general ML request"""
    try:
        # Extract request info
        request_id = message.get("request_id", "unknown")
        model_type = message.get("model_type", "random_forest")
        features = message.get("features", {})
        
        # Validate model type
        if model_type not in ["random_forest", "neural_network"]:
            await manager.send_personal_message(
                {
                    "type": "error",
                    "request_id": request_id,
                    "message": f"Unsupported model type: {model_type}"
                },
                websocket
            )
            return
            
        # Process request using ML service
        result = await ml_service.process_request(features, model_type)
        
        # Send response
        await manager.send_personal_message(
            {
                "type": "ml_response",
                "request_id": request_id,
                "result": result
            },
            websocket
        )
    except Exception as e:
        logger.error(f"Error handling ML request: {str(e)}")
        await manager.send_personal_message(
            {
                "type": "error",
                "request_id": message.get("request_id", "unknown"),
                "message": f"Error processing ML request: {str(e)}"
            },
            websocket
        )


async def start_ml_stream(websocket: WebSocket, model_type: str, message: Dict[str, Any]):
    """Start streaming ML predictions"""
    stream_id = message.get("stream_id", f"stream_{id(websocket)}")
    parameters = message.get("parameters", {})
    
    try:
        # Start streaming process with the ML service
        await ml_service.start_streaming(
            websocket=websocket,
            model_type=model_type,
            stream_id=stream_id,
            parameters=parameters
        )
        
        # Confirm stream started
        await manager.send_personal_message(
            {
                "type": "stream_status",
                "stream_id": stream_id,
                "status": "started",
                "model_type": model_type
            },
            websocket
        )
    except Exception as e:
        logger.error(f"Error starting ML stream: {str(e)}")
        await manager.send_personal_message(
            {
                "type": "error",
                "stream_id": stream_id,
                "message": f"Error starting ML stream: {str(e)}"
            },
            websocket
        )


async def stop_ml_stream(websocket: WebSocket, message: Dict[str, Any]):
    """Stop an active ML prediction stream"""
    stream_id = message.get("stream_id", None)
    
    if not stream_id:
        # If no specific stream ID, stop all streams for this client
        await ml_service.stop_stream_for_client(websocket)
        await manager.send_personal_message(
            {"type": "stream_status", "status": "all_stopped"},
            websocket
        )
    else:
        # Stop specific stream
        stopped = await ml_service.stop_stream(stream_id, websocket)
        await manager.send_personal_message(
            {
                "type": "stream_status",
                "stream_id": stream_id,
                "status": "stopped" if stopped else "not_found"
            },
            websocket
        )


async def handle_classification(websocket: WebSocket, model_type: str, message: Dict[str, Any]):
    """Process a single classification request"""
    request_id = message.get("request_id", "unknown")
    features = message.get("features", {})
    
    try:
        # Create request
        ml_request = MLClassificationRequest(
            features=features,
            model_type=model_type
        )
        
        # Process through ML service
        result = await ml_service.classify(ml_request)
        
        # Send response
        await manager.send_personal_message(
            {
                "type": "classification",
                "request_id": request_id,
                "result": {
                    "prediction": result.prediction,
                    "confidence": result.confidence,
                    "probabilities": result.probabilities
                }
            },
            websocket
        )
    except Exception as e:
        logger.error(f"Classification error: {str(e)}")
        await manager.send_personal_message(
            {
                "type": "error",
                "request_id": request_id,
                "message": f"Classification error: {str(e)}"
            },
            websocket
        )