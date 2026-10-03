from fastapi import WebSocket
from typing import List

class ConnectionManager:
    def __init__(self):
        # Store all active WebSocket connections
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        # Accept and store the new connection
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        # Remove connection from the list
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        # Send message to a specific client
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        # Send message to ALL connected clients
        for connection in self.active_connections:
            await connection.send_text(message)

# Create a single instance to use across your app
manager = ConnectionManager()
