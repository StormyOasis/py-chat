import socket
import threading
from core.constants import DEFAULT_BUFFER_SIZE, DEFAULT_TIMEOUT, DEFAULT_ROOM, DEFAULT_HOST, DEFAULT_PORT, DISCONNECT_FLAG
from data.message import Message
from data.clientsession import ClientSession
from data.room import Room
from typing import List
from argparse import ArgumentParser
from utils.utils import generateDefaultUserName, handleCommandMessage
import time

class ChatServer:
    # Chat server class for handling multiple client connections and message routing

    def __init__(self, host: str, port: int, timeout: int = DEFAULT_TIMEOUT):
        self.host = host
        self.port = port
        self.idleTimeout = timeout
        self.sessions: List[ClientSession] = []
        self.rooms = {DEFAULT_ROOM: Room(DEFAULT_ROOM)}
        self.serverSocket: socket.socket = None

    def start(self) -> None:
        self.lock = threading.Lock()
        if self.serverSocket is None:
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.serverSocket.bind((self.host, self.port))
            self.serverSocket.listen()
            print(f"Server listening on {self.host}:{self.port}")
            
        # Start idle user checker
        threading.Thread(target=self.handleIdledClients, daemon=True).start()
                        
        while True:
            # It's a server, run forever or until stopped
            conn, addr = self.serverSocket.accept()
            print(f"New connection from {addr}")
            session = ClientSession(connection=conn, address=str(addr), userName=f"{generateDefaultUserName()}", lastActive=None)
            session.lastActive = time.time()
            with self.lock:
                self.sessions.append(session)
                self.rooms[DEFAULT_ROOM].addUser(session)

            # We need a thread per client connection
            threading.Thread(target=self.processClientConnection, args=(session,), daemon=True).start()
    
    def handleIdledClients(self) -> None:
        while True:
            time.sleep(10)  # Check every 10 seconds
            currentTime = time.time()
            with self.lock:
                for session in self.sessions[:]:
                    if currentTime - session.lastActive > self.idleTimeout:
                        print(f"Disconnecting idle user {session.userName} from {session.address}")
                        self.disconnectClient(session)
    
    def processClientConnection(self, session: ClientSession) -> None:
        # This is now in it's own thread
        session.connection.sendall("Welcome to Py-Chat!\n".encode())
        
        while True:
            try:
                message = session.connection.recv(DEFAULT_BUFFER_SIZE).decode()
                if not message:
                    break
                session.lastActive = time.time()
                          
                if(message.startswith("/")):
                    # Don't wanna send commands to other users
                    isQuit = handleCommandMessage(session, message, self.lock, self.rooms)
                    if(isQuit):
                        break
                else:
                    newMessage = Message(session.userName, message.strip(), session.currentRoom)
                    self.sendAllInRoom(newMessage, session)                 
            except (ConnectionResetError, BrokenPipeError):
                break
        
        self.disconnectClient(session)
    
    def sendAllInRoom(self, message: Message, session: ClientSession) -> None:
        # Send message to all clients in the specified room
        formattedMessage = message.format() + "\n"
                
        with self.lock:
            room = self.rooms.get(session.currentRoom)
            if not room:
                return            
            for s in room.getSessions():
                if s != session:
                    try:
                        if not s.connection._closed:
                            s.connection.sendall(formattedMessage.encode())
                        else:
                            self.disconnectClient(s)                            
                    except Exception as e:
                        print(f"Error sending message to {s.userName}: {e}")
                        self.disconnectClient(s)
    
    def disconnectClient(self, session: ClientSession) -> None:                                     
        # Send disconnect message before closing
        if not session.connection._closed:
            try:
                session.connection.sendall(DISCONNECT_FLAG.encode())
                session.connection.close()  
            except:
                pass                  
                
        # Now remove from the session list, but we're going to need a lock
        with self.lock:
            if session in self.sessions:
                self.sessions.remove(session)
            if session.currentRoom in self.rooms:
                self.rooms[session.currentRoom].removeUser(session)                  
                
        print(f"Disconnected {session.userName} from {session.address}") 
    
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