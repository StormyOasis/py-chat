import socket
from datetime import datetime
from dataclasses import dataclass
 
@dataclass
class ClientSession:
    # Represents a session connected to the chat server
    connection: socket.socket
    address: str
    userName: str
    lastActive: datetime = None
    messageCount: int = 0
