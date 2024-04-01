import socket
import threading

# define the local host and port
HOST = "127.0.0.1"
PORT = 1738

# listen for message from server
def listen_for_messages_from_server(client):
    while 1:

        message = client.recv(2048).decode('utf-8')

        if message != '':
            username = message.split(":")[0]
            content = message.split(':')[1]

            print(f"[{username}] {content}")
        else:
            print("The message recevived is empty.")

# sends message to server
def send_message_to_server(client):
    while 1:
        message = input("Message: ")
        if message != '':
            client.sendall(message.encode())
        else:
            print("Message is empty.")
            exit(0)

# commuicates to the server
def communicate_to_server(client):
    username = input("Enter username: ")
    if username != '':
        client.sendall(username.encode())
    else:
        print("Username cannot be empty.")
        exit(0)
    
    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()

    send_message_to_server(client)

# main function
def main():

    # create socket object (IPv4, TCP) & bind the client to the host and port
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    # connect to the server
    try:
        client.connect((HOST,PORT))
        print("Successfully connected to server.")
    except:
        print("Unable to connect to the server {HOST} {PORT}")
    
    communicate_to_server(client)

# calling main
if __name__ == "__main__":
    main()