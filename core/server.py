import socket
import threading
from core.constants import DEFAULT_TIMEOUT, DEFAULT_ROOM, DEFAULT_HOST, DEFAULT_PORT
from data.message import Message
from data.clientsession import ClientSession
from data.room import Room
from typing import List
from argparse import ArgumentParser
from utils.utils import generateDefaultUserName
import time

class ChatServer:
    # Chat server class for handling multiple client connections and message routing

    def __init__(self, host: str, port: int, timeout: int = DEFAULT_TIMEOUT):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sessions: List[ClientSession] = []
        self.rooms = {DEFAULT_ROOM: Room(DEFAULT_ROOM)}
        self.serverSocket: socket.socket = None

    def start(self) -> None:
        if self.serverSocket is None:
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serverSocket.bind((self.host, self.port))
            self.serverSocket.listen()
            print(f"Server listening on {self.host}:{self.port}")
            
        while True:
            # It's a server, run forever or until stopped
            conn, addr = self.serverSocket.accept()
            print(f"New connection from {addr}")
            session = ClientSession(connection=conn, address=str(addr), userName=f"{generateDefaultUserName()}", lastActive=None, messageCount=0)
            session.lastActive = time.time()
            self.sessions.append(session)
            self.rooms[DEFAULT_ROOM].addUser(session)
    
            self.processClientConnection(session)
    
    def processClientConnection(self, session: ClientSession) -> None:
        session.connection.sendall("Welcome to Py-Chat!\n".encode())
    
    def stop(self) -> None:
        if self.serverSocket is not None:
            self.serverSocket.close()
            self.serverSocket = None
            print("Server stopped")
    
if __name__ == "__main__":
    parser = ArgumentParser(description="Start the server")
    parser.add_argument("--host", default=DEFAULT_HOST, help="Host address")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port number for server to listent on")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="Timeout in seconds")
    args = parser.parse_args()    
    
    server = ChatServer(args.host, args.port, args.timeout)
    server.start()