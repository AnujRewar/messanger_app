import socket
from tkinter import *
from threading import Thread

def send(listbox, entry):
    message = entry.get()
    if message:
        listbox.insert('end', "You: " + message)
        entry.delete(0, END)
        try:
            s.send(message.encode("utf-8"))
        except Exception as e:
            listbox.insert('end', f"Send error: {e}")

def receive_messages(listbox):
    while True:
        try:
            msg = s.recv(1024)
            if not msg:
                listbox.insert('end', "Server disconnected.")
                break
            listbox.insert('end', "Server: " + msg.decode("utf-8"))
        except Exception as e:
            listbox.insert('end', f"Receive error: {e}")
            break

def connect_to_server():
    try:
        s.connect((socket.gethostname(), 12345))
        listbox.insert('end', "Connected to server.")
        Thread(target=receive_messages, args=(listbox,), daemon=True).start()
    except Exception as e:
        listbox.insert('end', f"Connection error: {e}")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

root = Tk()
root.title("Client")

entry = Entry(root)
entry.pack(side=BOTTOM, fill=X)

listbox = Listbox(root, width=50, height=20)
listbox.pack()

send_button = Button(root, text="Send", command=lambda: send(listbox, entry))
send_button.pack(side=LEFT, expand=True, fill=X)

connect_button = Button(root, text="Connect", command=connect_to_server)
connect_button.pack(side=RIGHT, expand=True, fill=X)

root.mainloop()
