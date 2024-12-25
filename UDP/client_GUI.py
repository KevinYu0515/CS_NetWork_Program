import socket, sys, threading, struct, time
import tkinter as tk
from tkinter import messagebox

PORT = 8888
BUF_SIZE = 1024

class Client:
    def __init__(self, root, rip, rport) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rip = rip
        self.rport = rport
        self.number = 0
        self.id = 0
        self.window = root
        self.received = tuple()
        self.label = tk.Label(self.window, text="Enter a number to Server")
        self.entry = tk.Entry(self.window)
        self.messages_frame = tk.Frame(self.window, width=300, height=300)
        self.scrollbar = tk.Scrollbar(self.messages_frame, orient="vertical")
        self.scrollbar.pack(side='right', fill='y')   

        self.scrollbar.pack(side="right", fill="y")
        
        self.label.pack(pady=10)
        self.window.title("UDP Client")
        self.entry.pack(pady=10)
        self.send_button = tk.Button(self.window, text="Send", command=lambda: self.run(number=self.entry.get()))
        self.socket.connect((self.rip, self.rport))
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

    def run(self, number: str):
        if not number.isdigit():
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
            return

        self.number = number
        threading.Thread(target=self.receive_from_server, daemon=True).start()
    
    def send(self, number: str):
        s = struct.Struct('!' + 'I 15s')
        self.id += 1
        record = (self.id, number.encode('utf-8'))
        packed_data = s.pack(*record)

        self.socket.sendto(packed_data, (self.rip, self.rport))

    def receive_from_server(self):
        self.socket.settimeout(0.01)
        while True:
            s = struct.Struct('!' + 'I 15s')
            try:
                recv_data, (rip, rport) = self.socket.recvfrom(BUF_SIZE)
                unpacked_data = s.unpack(recv_data)
                n = unpacked_data[0]
                msg = unpacked_data[1].rstrip(b'\x00').decode()
                print('%d : Receive %dth message: (%s) from %s:%s' % (self.id, n, msg, str(rip), str(rport)))
                if msg and int(msg) <= 0:
                    messagebox.showinfo("Connection Closed", "The number is lower 0.")
                    self.socket.close()
                    break

                msg = int(msg)
                self.received = self.received + (f"Received number: {msg}", )
                self.menu.set(self.received)
                self.listbox.yview_moveto(1)
                msg -= 1
                time.sleep(1)
                self.send(str(msg))

            except socket.timeout:
                self.received = self.received + (f"\nTimeout!! Server did not respond in time. Retrying...", )
                self.menu.set(self.received)
                self.listbox.yview_moveto(1)
                msg = self.number
                self.send(str(msg))
                continue

            except Exception as e:
                # messagebox.showerror("Error", f"Error occurred: {e}")
                continue
            
            

if __name__ == "__main__":
    root = tk.Tk()
    client = Client(root, rip=socket.gethostbyname(sys.argv[1]), rport=PORT)
    root.mainloop()