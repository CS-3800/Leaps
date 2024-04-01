import socket
import threading

# define the local host and port
HOST = "127.0.0.1"
PORT = 1738
LISTENER_LIMIT = 5

def main():
    
    # create socket object (IPv4, TCP) & bind the server to the host and port
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    try:
        server.bind((HOST, PORT)) 
        print(f"Running the server on {HOST} {PORT}")
    except:
        print("Unable to bind to the host {HOST} and port {PORT}") 
    
    # number of maximum clients that can be connected
    server.listen(LISTENER_LIMIT) 

    # loop to accept incoming connections and to confirm connection
    while 1:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")

# calling main
if __name__ == "__main__":
    main()