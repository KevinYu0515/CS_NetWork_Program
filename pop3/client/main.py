import customtkinter as ctk
from gui.login import Login
import socket, sys

PORT = 110

if __name__ == '__main__':
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(((sys.argv[1] if len(sys.argv) >= 2 else '140.134.135.41') , PORT))
    reply = client_socket.recv(1024).decode('utf-8')
    print('Receive message: %s' % reply)

    root = ctk.CTk()
    app = Login(root, client_socket)
    root.mainloop()