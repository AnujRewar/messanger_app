import socket
from tkinter import *
from threading import Thread

def send(listbox, entry):
    message = entry.get()
    if message:
        listbox.insert('end', "Server: " + message)
        entry.delete(0, END)
        try:
            client.send(message.encode("utf-8"))
        except Exception as e:
            listbox.insert('end', f"Error sending: {e}")

def receive_messages(listbox):
    while True:
        try:
            msg = client.recv(1024)
            if not msg:
                listbox.insert('end', "Client disconnected.")
                break
            listbox.insert('end', "Client: " + msg.decode("utf-8"))
        except Exception as e:
            listbox.insert('end', f"Receive error: {e}")
            break

def start_server():
    global client
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 12345))
    s.listen(1)
    listbox.insert('end', "Waiting for client to connect...")
    client, addr = s.accept()
    listbox.insert('end', f"Client connected from {addr}")
    Thread(target=receive_messages, args=(listbox,), daemon=True).start()

root = Tk()
root.title("Server")

entry = Entry(root)
entry.pack(side=BOTTOM, fill=X)

listbox = Listbox(root, width=50, height=20)
listbox.pack()

send_button = Button(root, text="Send", command=lambda: send(listbox, entry))
send_button.pack(side=LEFT, expand=True, fill=X)

start_button = Button(root, text="Start Server", command=start_server)
start_button.pack(side=RIGHT, expand=True, fill=X)

root.mainloop()
