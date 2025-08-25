import uuid

def generateDefaultUserName() -> str:
    guid: str = str(uuid.uuid4())
    userName:str = f"guest_{guid[:8]}"
    return userName

