from select import select
import socket
import argparse
import sys
from core.constants import DEFAULT_HOST, DEFAULT_PORT, DEFAULT_BUFFER_SIZE, DISCONNECT_FLAG, QUIT_FLAG
import threading

stopEvent = threading.Event() #Event for stopping threads on sever disconect

def connectToServer(host: str, port: int):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((host, port))
    return clientSocket

def getMessagesFromServer(socket: socket.socket):
    while not stopEvent.is_set():
        try:
            message = socket.recv(DEFAULT_BUFFER_SIZE).decode().strip()               
            if not message:
                stopEvent.set() # Shut down the thread
                print("Server closed connection.")
                break
            if message == DISCONNECT_FLAG:
                stopEvent.set()
                break
            print(message)
        except Exception as e:
            stopEvent.set() # Shut down the thread
            print(f"Error receiving message: {e}")
            break      
            
def getInput(socket: socket.socket):
    # Loop until /quit is entered or server disconnects
    while not stopEvent.is_set():
        #try:
        #    message = input("")
        #except EOFError:
        #    stopEvent.set()
        #    break
        
        ready, _, _ = select([sys.stdin], [], [], 0.5)        

        if stopEvent.is_set():
            break

        if ready:
            message = sys.stdin.readline().strip()
            if(message == ""):
                continue
            
            if stopEvent.is_set():
                break        
                            
            try:
                socket.sendall(message.encode())
            except BrokenPipeError:
                stopEvent.set()   
                break        
            
            if message.startswith(QUIT_FLAG):            
                stopEvent.set()            
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
    recvThread = threading.Thread(target=getMessagesFromServer, args=(socket,), daemon=True).start()
    inputThread = threading.Thread(target=getInput, args=(socket,), daemon=True).start()
    
    stopEvent.wait() # Wait until one of the threads sets the stopEvent
            
    print("Stopping client...")
    
    try:
        sys.stdin.close()        
    except:
        pass    
    finally:
        socket.close()

    print("Client stopped.")

    
        