import socket
import argparse
from core.constants import DEFAULT_HOST, DEFAULT_PORT

def connectToServer(host: str, port: int):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((host, port))
    return clientSocket

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Py-Chat Client")
    parser.add_argument("--host", default=DEFAULT_HOST, help="Server host")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Server port")
    args = parser.parse_args()
    
    socket = connectToServer(args.host, args.port)
    print(f"Connected to Py-Chat server at {args.host}:{args.port}")