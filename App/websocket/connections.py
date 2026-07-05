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
    
    def disconnect(self, client_id: str) -> None:
        # Removes a WebSocket connection from the active connections dictionary
        if client_id in self.active_connections:
            del self.active_connections[client_id]
    