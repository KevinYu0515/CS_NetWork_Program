import xmlrpc.client
import os
from dotenv import load_dotenv
load_dotenv()

class App:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.proxy = xmlrpc.client.ServerProxy('http://' + os.getenv("HOSTNAME") + ':' + str(os.getenv("PORT")))
        
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