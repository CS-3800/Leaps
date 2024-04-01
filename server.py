import socket
import threading

# define the local host and port
HOST = "127.0.0.1"
PORT = 1738
LISTENER_LIMIT = 5
# list of all connected clients
active_clients = [] 

# listen to messages from the clients
def listen_for_messages(client, username):
    while 1:
        message = client.recv(2048).decode('utf-8')
        # check if the message is empty
        if message != '':
            final_msg = username + ": " + message
            send_messages_to_all(final_msg)
        else:
            print(f"The message sent from client {username} is empty.")

# send message to client
def send_message_to_client(client, message):
    client.sendall(message.encode())

# sends messages to all connected clients 
def send_messages_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1], message)

# handles clients
def client_handler(client):
    
    # server listen for the client username
    while 1:
        username = client.recv(2048).decode('utf-8')
        # check if client username is empty
        if username != '':
            active_clients.append((username, client))
            prompt_message = "SERVER: " + f"{username} added to the chat."
            send_messages_to_all(prompt_message)
            break
        else: 
            print("Client username is empty.")

    threading.Thread(target=listen_for_messages, args=(client, username, )).start()

# main function
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
    
        threading.Thread(target=client_handler, args=(client, )).start() 

# calling main
if __name__ == "__main__":
    main()