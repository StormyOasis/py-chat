from typing import Dict
import uuid

from data.clientsession import ClientSession
from data.room import Room

def generateDefaultUserName() -> str:
    guid: str = str(uuid.uuid4())
    userName:str = f"guest_{guid[:8]}"
    return userName

def changeRoom(session: ClientSession, newRoom: str, rooms) -> None:
    # Change the room creating the room if it doesn't exist
    oldRoom = session.currentRoom
    if oldRoom in rooms:
        rooms[oldRoom].removeUser(session)
        
    if newRoom not in rooms:
        rooms[newRoom] = Room(newRoom)
        
    rooms[newRoom].addUser(session)
    session.currentRoom = newRoom

def handleCommandMessage(session: ClientSession, message: str, lock, rooms) -> bool:
    # Handle commands like /room, /help, /user, /quit
    isQuit: bool = False
    
    try:    
        if message.startswith("/quit"):
            session.connection.sendall("Goodbye!\n".encode())
            isQuit = True
        elif message.startswith("/help"):
            helpMessage = (
                "Available commands:\n"
                "/help - Show this help message\n"
                "/user <newname> - Change your username\n"
                "/room <roomname> - Change your chat room\n"
                "/quit - Disconnect from the server\n"
            )
            session.connection.sendall(helpMessage.encode())
        elif message.startswith("/user"):
            parts = message.split(maxsplit=1)
            if(len(parts) == 2):
                newName = parts[1].strip()
                if newName:
                    oldName = session.userName
                    session.userName = newName
                    session.connection.sendall(f"Username changed from {oldName} to {newName}\n".encode())
                else:
                    session.connection.sendall("Usage: /user <newname>\n".encode())
        elif message.startswith("/room"):
            parts = message.split(maxsplit=1)
            if(len(parts) == 2):
                newRoom = parts[1].strip()
                if newRoom:
                    oldRoom = session.currentRoom
                    with lock:
                        changeRoom(session, newRoom, rooms)                    
                        session.connection.sendall(f"Room changed from {oldRoom} to {newRoom}\n".encode())
                else:
                    session.connection.sendall("Usage: /room <roomname>\n".encode())
             
    except Exception as e: 
        print(f"Error handling command: {e}")
        
    return isQuit