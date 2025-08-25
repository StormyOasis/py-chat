import socket
import threading
from core.constants import DEFAULT_TIMEOUT, DEFAULT_ROOM
from data.message import Message
from data.clientsession import ClientSession
from data.room import Room
from typing import List

class ChatServer:
    # Chat server class for handling multiple client connections and message routing

    def __init__(self, host: str, port: int, timeout: int = DEFAULT_TIMEOUT):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sessions = List[ClientSession] = []
        self.rooms = {DEFAULT_ROOM: Room(DEFAULT_ROOM)}

    def start(self) -> None:
        pass
    
    def stop(self) -> None:
        pass
    
if __name__ == "__main__":
    server = ChatServer()
    server.start()