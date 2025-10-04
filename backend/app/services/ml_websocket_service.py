"""
ML WebSocket service for real-time model predictions and streaming.
"""
import asyncio
import logging
import random
import time
from typing import Dict, Any, Optional, List
from fastapi import WebSocket

from app.models.schemas import MLClassificationRequest, MLClassificationResponse

logger = logging.getLogger(__name__)


class MLWebSocketService:
    """Service for ML model predictions with WebSocket streaming support"""
    
    def __init__(self):
        self.active_streams: Dict[str, asyncio.Task] = {}
        self.client_streams: Dict[WebSocket, List[str]] = {}
        
    async def classify(self, request: MLClassificationRequest) -> MLClassificationResponse:
        """
        Perform classification with the specified ML model
        
        Args:
            request: Classification request with features and model type
            
        Returns:
            Classification result
        """
        # This is a mock implementation similar to the one in ml.py routes
        # In a real app, this would use actual ML models
        features = request.features
        model_type = request.model_type
        
        # Mock classification logic
        confidence_score = 0.75 + (hash(str(features)) % 100) / 400  # Random confidence 0.75-1.0
        
        # Simple rule-based mock classification
        period = features.get("period", 0)
        radius = features.get("radius", 0)
        
        if period > 300 or radius > 10:
            prediction = "FALSE_POSITIVE"
            confidence = max(0.6, confidence_score - 0.1)
        elif 1 < period < 50 and 0.5 < radius < 4:
            prediction = "CONFIRMED"
            confidence = confidence_score
        else:
            prediction = "CANDIDATE"
            confidence = confidence_score - 0.2
        
        probabilities = {
            "CONFIRMED": confidence if prediction == "CONFIRMED" else (1 - confidence) / 2,
            "CANDIDATE": confidence if prediction == "CANDIDATE" else (1 - confidence) / 2,
            "FALSE_POSITIVE": confidence if prediction == "FALSE_POSITIVE" else (1 - confidence) / 2
        }
        
        # Normalize probabilities
        total_prob = sum(probabilities.values())
        if total_prob > 0:
            probabilities = {k: v / total_prob for k, v in probabilities.items()}
        
        # Simulate processing time
        await asyncio.sleep(0.1)
        
        return MLClassificationResponse(
            prediction=prediction,
            confidence=confidence,
            probabilities=probabilities
        )
    
    async def process_request(self, features: Dict[str, float], model_type: str) -> Dict[str, Any]:
        """
        Process an ML request and return the result
        
        Args:
            features: Feature values for prediction
            model_type: Type of ML model to use
            
        Returns:
            Prediction result
        """
        request = MLClassificationRequest(
            features=features,
            model_type=model_type
        )
        
        result = await self.classify(request)
        
        return {
            "prediction": result.prediction,
            "confidence": result.confidence,
            "probabilities": result.probabilities,
            "model_used": model_type,
            "timestamp": time.time()
        }
    
    async def process_streaming_request(
        self,
        features: Dict[str, float],
        model_type: str,
        queue: asyncio.Queue
    ) -> None:
        """
        Process an ML request with streaming updates
        
        Args:
            features: Feature values for prediction
            model_type: Type of ML model to use
            queue: Queue for sending streaming updates
        """
        # Start with status update
        await queue.put({
            "type": "status",
            "status": "processing",
            "progress": 0.0
        })
        
        # Simulate feature extraction
        await asyncio.sleep(0.1)
        await queue.put({
            "type": "status",
            "status": "processing",
            "progress": 0.2,
            "step": "feature_extraction"
        })
        
        # Simulate model loading
        await asyncio.sleep(0.1)
        await queue.put({
            "type": "status",
            "status": "processing",
            "progress": 0.4,
            "step": "model_loading"
        })
        
        # Simulate prediction
        await asyncio.sleep(0.2)
        
        # Generate result
        request = MLClassificationRequest(
            features=features,
            model_type=model_type
        )
        result = await self.classify(request)
        
        # Send progress update
        await queue.put({
            "type": "status",
            "status": "processing",
            "progress": 0.7,
            "step": "prediction"
        })
        
        # Send intermediate results
        await queue.put({
            "type": "partial_result",
            "prediction": result.prediction,
            "confidence": round(result.confidence * 0.9, 2),  # Slightly lower confidence for partial result
            "model_used": model_type
        })
        
        # Simulate post-processing
        await asyncio.sleep(0.2)
        
        # Send final results
        await queue.put({
            "type": "result",
            "prediction": result.prediction,
            "confidence": result.confidence,
            "probabilities": result.probabilities,
            "model_used": model_type,
            "timestamp": time.time()
        })
    
    async def start_streaming(
        self,
        websocket: WebSocket,
        model_type: str,
        stream_id: str,
        parameters: Dict[str, Any]
    ) -> None:
        """
        Start streaming ML predictions to a client
        
        Args:
            websocket: Client WebSocket
            model_type: Type of ML model to use
            stream_id: Unique ID for the stream
            parameters: Stream parameters
        """
        # Stop existing stream with this ID if any
        await self.stop_stream(stream_id, websocket)
        
        # Create data queue for this stream
        data_queue = asyncio.Queue()
        
        # Set up parameters
        interval = parameters.get("interval", 1.0)  # Default 1 second between updates
        duration = parameters.get("duration", 30)   # Default 30 seconds
        feature_ranges = parameters.get("feature_ranges", {
            "period": [0.5, 100.0],
            "radius": [0.1, 15.0],
            "mass": [0.1, 20.0],
            "temperature": [200, 2000]
        })
        
        # Start streaming task
        stream_task = asyncio.create_task(
            self._stream_predictions(
                websocket=websocket,
                model_type=model_type,
                stream_id=stream_id,
                data_queue=data_queue,
                interval=interval,
                duration=duration,
                feature_ranges=feature_ranges
            )
        )
        
        # Store stream task reference
        self.active_streams[stream_id] = stream_task
        
        # Associate stream with client
        if websocket not in self.client_streams:
            self.client_streams[websocket] = []
        self.client_streams[websocket].append(stream_id)
    
    async def stop_stream(self, stream_id: str, websocket: Optional[WebSocket] = None) -> bool:
        """
        Stop an active prediction stream
        
        Args:
            stream_id: ID of the stream to stop
            websocket: Optional WebSocket to verify client ownership
            
        Returns:
            True if a stream was stopped, False otherwise
        """
        if stream_id not in self.active_streams:
            return False
            
        # If websocket provided, verify it owns this stream
        if websocket is not None:
            if (websocket not in self.client_streams or 
                stream_id not in self.client_streams[websocket]):
                return False
        
        # Cancel the task
        task = self.active_streams[stream_id]
        if not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
                
        # Clean up references
        if websocket is not None and websocket in self.client_streams:
            if stream_id in self.client_streams[websocket]:
                self.client_streams[websocket].remove(stream_id)
        
        # Remove from active streams
        if stream_id in self.active_streams:
            del self.active_streams[stream_id]
            
        return True
    
    async def stop_stream_for_client(self, websocket: WebSocket) -> None:
        """
        Stop all streams for a specific client
        
        Args:
            websocket: Client WebSocket
        """
        if websocket not in self.client_streams:
            return
            
        # Get all streams for this client
        stream_ids = self.client_streams[websocket].copy()
        
        # Stop each stream
        for stream_id in stream_ids:
            await self.stop_stream(stream_id, websocket)
            
        # Clean up client reference
        if websocket in self.client_streams:
            del self.client_streams[websocket]
    
    async def _stream_predictions(
        self,
        websocket: WebSocket,
        model_type: str,
        stream_id: str,
        data_queue: asyncio.Queue,
        interval: float,
        duration: int,
        feature_ranges: Dict[str, List[float]]
    ) -> None:
        """
        Stream periodic ML predictions
        
        Args:
            websocket: Client WebSocket
            model_type: Type of ML model
            stream_id: Stream ID
            data_queue: Queue for sending data to the client
            interval: Time between predictions
            duration: Total streaming duration in seconds
            feature_ranges: Value ranges for features
        """
        try:
            from app.websockets import manager
            
            start_time = time.time()
            end_time = start_time + duration
            
            # Send stream start notification
            await manager.send_personal_message(
                {
                    "type": "stream_data",
                    "stream_id": stream_id,
                    "event": "started",
                    "model_type": model_type,
                    "timestamp": time.time()
                },
                websocket
            )
            
            # Continue streaming until duration expires
            while time.time() < end_time:
                # Generate random features within specified ranges
                features = {}
                for feature, range_values in feature_ranges.items():
                    min_val, max_val = range_values
                    features[feature] = min_val + random.random() * (max_val - min_val)
                
                # Get prediction for these features
                request = MLClassificationRequest(
                    features=features,
                    model_type=model_type
                )
                result = await self.classify(request)
                
                # Create stream data message
                stream_data = {
                    "type": "stream_data",
                    "stream_id": stream_id,
                    "prediction": result.prediction,
                    "confidence": result.confidence,
                    "features": features,
                    "timestamp": time.time(),
                    "time_remaining": round(end_time - time.time(), 1)
                }
                
                # Send to client
                await manager.send_personal_message(stream_data, websocket)
                
                # Wait for next interval
                await asyncio.sleep(interval)
                
            # Send stream end notification
            await manager.send_personal_message(
                {
                    "type": "stream_data",
                    "stream_id": stream_id,
                    "event": "completed",
                    "model_type": model_type,
                    "timestamp": time.time()
                },
                websocket
            )
            
        except asyncio.CancelledError:
            logger.info(f"Stream {stream_id} was cancelled")
            
            # Notify client of cancellation if possible
            try:
                from app.websockets import manager
                await manager.send_personal_message(
                    {
                        "type": "stream_data",
                        "stream_id": stream_id,
                        "event": "cancelled",
                        "timestamp": time.time()
                    },
                    websocket
                )
            except Exception:
                pass
                
            raise
            
        except Exception as e:
            logger.error(f"Error in prediction stream {stream_id}: {str(e)}")
            
            # Notify client of error if possible
            try:
                from app.websockets import manager
                await manager.send_personal_message(
                    {
                        "type": "error",
                        "stream_id": stream_id,
                        "message": f"Stream error: {str(e)}",
                        "timestamp": time.time()
                    },
                    websocket
                )
            except Exception:
                pass
        
        finally:
            # Clean up references
            if stream_id in self.active_streams:
                del self.active_streams[stream_id]
                
            if websocket in self.client_streams and stream_id in self.client_streams[websocket]:
                self.client_streams[websocket].remove(stream_id)