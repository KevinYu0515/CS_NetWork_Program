import socket
from dotenv import load_dotenv
load_dotenv()

BUFF_SIZE = 4096
class App:
    def __init__(self, root, user, client_socket):
        self.root = root
        self.root.title("Mail Recevier")
        self.user = user
        self.socket: socket.socket = client_socket
        self.root.protocol("WM_DELETE_WINDOW", self.onclosing)
        
    def center_window(self, master, width, height):
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        master.geometry(f"{width}x{height}+{x}+{y}")

    def on_hover(self, event):
        event.widget.configure(cursor="hand2")

    def on_leave(self, event):
        event.widget.configure(cursor="")

    def switch_screen(self, before_screen, after_screen):
        before_screen.pack_forget()
        after_screen(self.root, self.user)

    def generated_cmd(self, cmd):
        return cmd +'\r\n'
    
    def send_and_recevie(self, cmd):
        self.socket.send(self.generated_cmd(cmd).encode('utf-8'))

        first_chunk = self.socket.recv(BUFF_SIZE)
        if not first_chunk.decode('utf-8').startswith('+OK'):
            raise Exception(f"Error: Received an invalid response '{first_chunk}'")
        
        reply = first_chunk
        return reply

    def onclosing(self):
        self.send_and_recevie("QUIT")
        self.root.destroy()