import socket
import threading
from core.constants import DEFAULT_TIMEOUT, DEFAULT_ROOM, DEFAULT_HOST, DEFAULT_PORT
from data.message import Message
from data.clientsession import ClientSession
from data.room import Room
from typing import List
from argparse import ArgumentParser

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
    parser = ArgumentParser(description="Start the server")
    parser.add_argument("--host", default=DEFAULT_HOST, help="Host address")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port number for server to listent on")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="Timeout in seconds")
    args = parser.parse_args()    
    
    server = ChatServer(args.host, args.port, args.timeout)
    server.start()