import socket
import threading
import tkinter as tk
import time
import re
import base64
from tkinter import scrolledtext
from tkinter import messagebox
# from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad

# Server host and port
HOST = '127.0.0.1'
PORT = 1738

# Encryption key (must be 16, 24, or 32 bytes long)
KEY = b'my_secret_key_12'

# Color constants
DARK_GRAY = '#333333'
MEDIUM_GRAY = '#666666'
LIGHT_GRAY = '#999999'
WHITE = '#FFFFFF'
BUTTON_GRAY = '#555555'  # Dark gray
BUTTON_GREEN = '#5CB85C'  # Green
BUTTON_ORANGE = '#F0AD4E'  # Orange
BUTTON_BLUE = '#3E92CC'    # Blue

# Font specifications
FONT = ("Open Sans", 17)
BUTTON_FONT = ("Open Sans", 15)
SMALL_FONT = ("Open Sans", 13)

# Main Tkinter window
root = tk.Tk()
root.title("Messenger Client")
root.geometry("650x600")
root.resizable(False, False)
root.configure(bg=DARK_GRAY)


#image path
image_path = "tran.png"
image = tk.PhotoImage(file=image_path)

#resize image
resized_image = image.subsample(3, 4)

# Socket initialization
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# AES encryption function
def encrypt_message(message):
    cipher = AES.new(KEY, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return iv + ct

# Function to show emoticons window
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
        button = tk.Button(emoticons_window, text=emoticon, font=("Open Sans", 12), command=lambda e=emoticon: add_to_message(e), bg=BUTTON_GRAY)
        button.pack()

# Regular expression pattern to match URLs
URL_PATTERN = r'(https?://\S+)'

def add_message(message):
    message_box.config(state=tk.NORMAL)
    
    # Search for URLs in the message
    matches = re.finditer(URL_PATTERN, message)
    last_end = 0
    
    for match in matches:
        start, end = match.span()

        message_box.insert(tk.END, message[last_end:start])
        
        # Add clickable link
        url = message[start:end]
        message_box.insert(tk.END, url, ('link', url))
        message_box.tag_bind('link', '<Button-1>', lambda event, u=url: open_url(u))
        
        # make link blue and underlined
        message_box.tag_config('link', foreground='blue', underline=True)
        
        last_end = end
    
    message_box.insert(tk.END, message[last_end:] + '\n', 'normal')
    message_box.config(state=tk.DISABLED)

# Function to open the URL when clicked
def open_url(url):
    import webbrowser
    webbrowser.open(url)

# Function to connect to the server
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

# Function to send message
def send_message():
    message = message_textbox.get()
    if message != '':
        timestamp = time.strftime('%Y-%m-%d %I:%M:%S %p')  # timestamp 
        encrypted_message = encrypt_message(f"{message} \n [{timestamp}]")  # encrypt message
        client.sendall(encrypted_message.encode())
        message_textbox.delete(0, len(message))
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")


# Function to clear default message in message textbox
def clear_default_message(event):
    if message_textbox.get() == "Type Here...":
        message_textbox.delete(0, tk.END)
        message_textbox.config(fg="black")  # Change text color when default message is cleared

# Function to restore default message in message textbox
def restore_default_message(event):
    if message_textbox.get() == "":
        message_textbox.insert(0, "Type Here...")
        message_textbox.config(fg="gray")  # Change text color for default message

# Function to change text color in message textbox
def change_color(color):
    message_textbox.config(fg=color)

# Function to show color options
def show_color_options():
    # Create a Toplevel window for color options
    color_options_window = tk.Toplevel(root)
    color_options_window.title("Choose a Color")

    # List of color options
    colors = ["red", "green", "blue", "yellow", "orange", "purple"]

    # Create buttons for each color option
    for color in colors:
        color_button = tk.Button(color_options_window, text=color.capitalize(), command=lambda c=color: change_color(c), bg=BUTTON_GRAY)
        color_button.pack()



# Create and configure the main frame
main_frame = tk.Frame(root, bg=DARK_GRAY)
main_frame.grid(row=0, column=0, sticky="nsew")

# Configure grid weights
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
main_frame.grid_rowconfigure(1, weight=1)

# Top Frame
top_frame = tk.Frame(main_frame, bg=MEDIUM_GRAY)
top_frame.grid(row=0, column=0, sticky="ew")

# Middle Frame
middle_frame = tk.Frame(main_frame, bg=MEDIUM_GRAY)
middle_frame.grid(row=1, column=0, sticky="nsew")

# Bottom Frame
bottom_frame = tk.Frame(main_frame, bg=MEDIUM_GRAY)
bottom_frame.grid(row=2, column=0, sticky="ew")

#Frog Picture
username_label = tk.Label(top_frame, image = resized_image, bg = MEDIUM_GRAY)
username_label.grid(row=0, column=0, padx=5)

# Username Label
username_label = tk.Label(top_frame, text="Enter name:", font=FONT, bg=MEDIUM_GRAY, fg=WHITE)
username_label.grid(row=0, column=1, padx=10)

# Username Textbox
username_textbox = tk.Entry(top_frame, font=FONT, bg=LIGHT_GRAY, fg=DARK_GRAY)
username_textbox.grid(row=0, column=2)

# Connect Button
username_button = tk.Button(top_frame, text="Connect", font=BUTTON_FONT, bg=BUTTON_GRAY, fg=WHITE, command=connect)
username_button.grid(row=0, column=3, padx=15)

# Message Textbox
message_textbox = tk.Entry(bottom_frame, font=FONT, bg=LIGHT_GRAY, fg=DARK_GRAY)
message_textbox.insert(0, "Type Here...")
message_textbox.bind("<FocusIn>", clear_default_message)
message_textbox.bind("<FocusOut>", restore_default_message)
message_textbox.grid(row=0, column=0, padx=10)

# Emoticons Button
emotes_frame = tk.Button(bottom_frame, text="😊", font=BUTTON_FONT, bg=BUTTON_GRAY, fg=WHITE, command=show_emoticons)
emotes_frame.grid(row=0, column=1, padx=(10, 0))

# Color Button
color_frame = tk.Button(bottom_frame, text="Color", font=BUTTON_FONT, bg=BUTTON_GRAY, fg=WHITE, command=show_color_options)
color_frame.grid(row=0, column=2, padx=10)

# Send Button
message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=BUTTON_GRAY, fg=WHITE, command=send_message)
message_button.grid(row=0, column=3, padx=(0, 10))

# Message Box
message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=LIGHT_GRAY, fg=DARK_GRAY)
message_box.config(state=tk.DISABLED)
message_box.grid(row=0, column=0)

# Function to listen for messages from the server
def listen_for_messages_from_server(client):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split("~")[0]
            content = message.split('~')[1]

            add_message(f"[{username}] {content}")
        else:
            messagebox.showerror("Error", "Message received from client is empty")

# Main function
def main():
    root.mainloop()

# Entry point of the program
if __name__ == '__main__':
    main()
