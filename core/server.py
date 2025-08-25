import socket
import threading
from core.constants import DEFAULT_BUFFER_SIZE, DEFAULT_TIMEOUT, DEFAULT_ROOM, DEFAULT_HOST, DEFAULT_PORT
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
        self.lock = threading.Lock()
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

            # We need a thread per client connection
            threading.Thread(target=self.processClientConnection, args=(session,), daemon=True).start()
    
    def processClientConnection(self, session: ClientSession) -> None:
        # This is now in it's own thread
        session.connection.sendall("Welcome to Py-Chat!\n".encode())
        
        while True:
            try:
                message = session.connection.recv(DEFAULT_BUFFER_SIZE).decode()
                if not message:
                    break
                session.lastActive = time.time()
                          
                if(message.startswith("/quit")):
                    # Don't wanna send the /quit to other users
                    break                         
                else:
                    newMessage = Message(session.userName, message.strip(), session.currentRoom)
                    self.sendAllInRoom(newMessage, session)
                    session.messageCount += 1                    
            except ConnectionResetError:
                break
        
        self.disconnectClient(session)
    
    def sendAllInRoom(self, message: Message, session: ClientSession) -> None:
        # Send message to all clients in the specified room
        formattedMessage = message.format() + "\n"
        for s in self.rooms[session.currentRoom].sessions:
            if s != session:
                s.connection.sendall(formattedMessage.encode())
    
    def disconnectClient(self, session: ClientSession) -> None:
        print(f"Disconnecting {session.userName} from {session.address}")
        session.connection.close()
        
        # Now remove from the session list, but we're going to need a lock
        with self.lock:
            if session in self.sessions:
                self.sessions.remove(session)
            if session.currentRoom in self.rooms:
                self.rooms[session.currentRoom].removeUser(session)
    
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