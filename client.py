import socket
import threading

# define the local host and port
HOST = "127.0.0.1"
PORT = 1738

def main():

    # create socket object (IPv4, TCP) & bind the client to the host and port
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    # connect to the server
    try:
        client.connect((HOST,PORT))
        print("Successfully cnnected to server.")
    except:
        print("Unable to connect to the server {HOST} {PORT}")

# calling main
if __name__ == "__main__":
    main()