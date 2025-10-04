"""
WebSocket package initialization.
"""
from app.websockets.connection_manager import manager

# Export the WebSocket manager
__all__ = ["manager"]