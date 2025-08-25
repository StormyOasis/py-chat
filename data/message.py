from dataclasses import dataclass
import time

@dataclass
class Message:
    # Data structure representing a chat message
    sender: str
    text: str
    room: str = None
    
    def format(self) -> str:
        # Format message and add timestamp and user name
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        return f"[{timestamp}] {self.sender}@{self.room}: {self.text}"