from typing import List

from data.clientsession import ClientSession

class Room:
    # Data structure representing a chat room with multiple users

    def __init__(self, name: str):
        self.name: str = name
        self.sessions: List[ClientSession] = []
        
        
    def addUser(self, session: ClientSession) -> None:
        # Add session to room
        if session not in self.sessions:
            self.sessions.append(session)
            
    def removeUser(self, session: ClientSession) -> None:
        # Removve session from room
        if session in self.sessions:
            self.sessions.remove(session)
