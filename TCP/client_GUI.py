import socket, sys, threading
import tkinter as tk
from tkinter import messagebox

PORT = 8888
BUF_SIZE = 1024

class Client:
    def __init__(self, root, IP, PORT) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.window = root
        self.received = tuple()
        self.label = tk.Label(self.window, text="Enter a number to Server")
        self.entry = tk.Entry(self.window)
        self.messages_frame = tk.Frame(self.window, width=300, height=300)
        self.scrollbar = tk.Scrollbar(self.messages_frame, orient="vertical")
        self.scrollbar.pack(side='right', fill='y')   

        self.scrollbar.pack(side="right", fill="y")
        
        self.label.pack(pady=10)
        self.window.title("TCP Client")
        self.entry.pack(pady=10)
        self.send_button = tk.Button(self.window, text="Send", command=lambda: self.run(number=self.entry.get()))
        self.socket.connect((IP, PORT))
        self.send_button.pack(pady=10)
        self.messages_frame.pack(pady=10)

        self.menu = tk.StringVar()
        self.menu.set(self.received)
        self.listbox = tk.Listbox(self.messages_frame, listvariable=self.menu, width=100, height=100, yscrollcommand=self.scrollbar.set)
        self.listbox.pack(side='left', fill='y')
        self.scrollbar.config(command = self.listbox.yview)

        self.center_window(600, 600)

    def center_window(self, width, height):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def update_scroll_region(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def run(self, number):
        if not number.isdigit():
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
            return

        self.socket.sendall(number.encode())
        threading.Thread(target=self.receive_from_server, daemon=True).start()

    def receive_from_server(self):
        while True:
            try:
                data = self.socket.recv(BUF_SIZE).decode()
                if not data or int(data) <= 0:
                    messagebox.showinfo("Connection Closed", "Number reached 0. Connection closed.")
                    self.socket.close()
                    break

                number = int(data)
                number -= 1
                self.received = self.received + (f"Received number: {number}", )
                self.menu.set(self.received)
                self.listbox.yview_moveto(1)
                self.socket.sendall(str(number).encode())
            except Exception as e:
                messagebox.showerror("Error", f"Error occurred: {e}")
                break

if __name__ == "__main__":
    root = tk.Tk()
    client = Client(root, IP=socket.gethostbyname(sys.argv[1]), PORT=PORT)
    root.mainloop()