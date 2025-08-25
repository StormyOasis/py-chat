import threading
from typing import List

from data.clientsession import ClientSession

class Room:
    # Data structure representing a chat room with multiple users

    def __init__(self, name: str):
        self.name: str = name
        self.sessions: List[ClientSession] = []
        self.lock = threading.Lock()
        
    def addUser(self, session: ClientSession) -> None:
        # Add session to room
        with self.lock:
            if session not in self.sessions:
                self.sessions.append(session)
            
    def removeUser(self, session: ClientSession) -> None:
        # Removve session from room
        with self.lock:
            if session in self.sessions:
                self.sessions.remove(session)
                
    def getSessions(self):
        with self.lock:
            return list(self.sessions)  # Return copy    
