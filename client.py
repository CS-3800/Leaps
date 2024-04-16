# import required modules
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

HOST = '127.0.0.1'
PORT = 1738

DARK_GREEN = '#22dc70'
MEDIUM_ORANGE = '#f1b50e'
OCEAN_BLUE = '#06d1fa'
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Lao UI", 15)
SMALL_FONT = ("Lao UI", 13)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def show_emoticons():
    # Create a Toplevel window
    emoticons_window = tk.Toplevel(root)
    emoticons_window.geometry("200x400")
    emoticons_window.title("Emoticons")

    # Create a list of emoticons
    emoticons = ["😊", "😂", "😍", "😎", "😜", "😇", "😘", "🥳", "🤩"]
    def add_to_message(emote):
        message_textbox.insert(tk.END, emote)
    # Display the list of emoticons
    for emoticon in emoticons:
        button = tk.Button(emoticons_window, text=emoticon, font=("Arial", 12), command=lambda e=emoticon: add_to_message(e))
        button.pack()


def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)

def connect():

    # try except block
    try:

        # Connect to the server
        client.connect((HOST, PORT))
        print("Successfully connected to server")
        add_message("[SERVER] Successfully connected to the server")
    except:
        messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}")

    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")

    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

def send_message():
    message = message_textbox.get()
    if message != '':
        client.sendall(message.encode())
        message_textbox.delete(0, len(message))
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")

def clear_default_message(event):
    if message_textbox.get() == "Type Here...":
        message_textbox.delete(0, tk.END)
        message_textbox.config(fg="black")  # Change text color when default message is cleared

def restore_default_message(event):
    if message_textbox.get() == "":
        message_textbox.insert(0, "Type Here...")
        message_textbox.config(fg="gray")  # Change text color for default message

root = tk.Tk()
root.geometry("600x600")
root.title("Messenger Client")
root.resizable(False, False)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREEN)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height=400, bg=MEDIUM_ORANGE)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREEN)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

username_label = tk.Label(top_frame, text="Enter name:", font=FONT, bg=DARK_GREEN, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_ORANGE, fg=WHITE, width=23)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text="Connect", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect)
username_button.pack(side=tk.LEFT, padx=15)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_ORANGE, fg=WHITE, width=35)
message_textbox.insert(0, "Type Here...")
message_textbox.bind("<FocusIn>", clear_default_message)
message_textbox.bind("<FocusOut>", restore_default_message)
message_textbox.pack(side=tk.LEFT, padx=10)

emotes_frame = tk.Button(bottom_frame, text="😊", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=show_emoticons)
emotes_frame.pack(side=tk.LEFT)

message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_message)
message_button.pack(side=tk.LEFT, padx=10)

message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_ORANGE, fg=WHITE, width=67, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)


def listen_for_messages_from_server(client):

    while 1:

        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split("~")[0]
            content = message.split('~')[1]

            add_message(f"[{username}] {content}")
            
        else:
            messagebox.showerror("Error", "Message recevied from client is empty")

# main function
def main():

    root.mainloop()
    
if __name__ == '__main__':
    main()