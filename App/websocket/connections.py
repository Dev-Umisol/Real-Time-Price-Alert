from fastapi import WebSocket

# Allows new connections to be accepted and stored in a dictionary, where each connection is associated with a unique client ID.
class ConnectionManager:
    # Manages active WebSocket connections
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
    
    # Connects a new WebSocket connection and stores it in the active connections dictionary
    async def connect(self, websocket: WebSocket, client_id: str) -> None:
        await websocket.accept()
        self.active_connections[client_id] = websocket
    
    # Disconnects a WebSocket connection and removes it from the active connections dictionary
    def disconnect(self, client_id: str) -> None:
        # Removes a WebSocket connection from the active connections dictionary
        if client_id in self.active_connections:
            del self.active_connections[client_id]
    
    # Sends a notification message to a specific WebSocket connection by client_id
    async def send_notification(self, client_id: str, message: str) -> None:
        # Sends a message to a specific WebSocket connection if it exists in the active connections dictionary
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)