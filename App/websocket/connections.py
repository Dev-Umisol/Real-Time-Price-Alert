from fastapi import WebSocket

class ConnectionManager:
    # Manages active WebSocket connections
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
    
    # Connects a new WebSocket connection and stores it in the active connections dictionary
    async def connect(self, websocket: WebSocket, client_id: str) -> None:
        await websocket.accept()
        self.active_connections[client_id] = websocket
    