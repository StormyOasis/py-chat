import socket
import argparse
from core.constants import DEFAULT_HOST, DEFAULT_PORT, DEFAULT_BUFFER_SIZE, QUIT_FLAG
import threading

def connectToServer(host: str, port: int):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((host, port))
    return clientSocket

def getMessagesFromServer(socket: socket.socket):
    while True:
        try:
            message = socket.recv(DEFAULT_BUFFER_SIZE).decode()
            if(not message):
                break
            print(message)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Py-Chat Client")
    parser.add_argument("--host", default=DEFAULT_HOST, help="Server host")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Server port")
    args = parser.parse_args()
    
    socket = connectToServer(args.host, args.port)
    print(f"Connected to Py-Chat server at {args.host}:{args.port}")
    
    # Below loop is for sending messages to server, not receiving messages
    # First we need to spawn a thread to listen for incoming messages from server
    threading.Thread(target=getMessagesFromServer, args=(socket,), daemon=True).start()
    
    # Loop until /quit is entered
    while True:
        message = input("> ")
        if(message.strip() == ""):
            continue
        socket.sendall(message.encode())
        if message.startswith(QUIT_FLAG):            
            break
        
    print("Disconnecting from server...")
    socket.close()
        