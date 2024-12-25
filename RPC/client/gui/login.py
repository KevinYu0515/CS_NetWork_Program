from . import App
import customtkinter as ctk
from .chatroom import ChatRoom
import os
from dotenv import load_dotenv
load_dotenv()

class Login(App):
    def __init__(self, root):
        super().__init__(root, None)
        self.root = root
        self.root.title("ChatRoom")
        self.width = int(os.getenv("ROOT_WIDTH"))
        self.height = int(os.getenv("ROOT_HEIGHT"))

        # login root grid
        self.root.geometry(f"{self.width}x{self.height}")
        self.center_window(self.root, self.width, self.height) 
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # login frame
        self.login_frame = ctk.CTkFrame(self.root, width=240, height=200, corner_radius=10)
        self.login_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.login_label = ctk.CTkLabel(self.login_frame, text="Enter your username")
        self.login_label.grid(row=0, column=0, pady=(20, 0))  # Add padding above the label

        self.username_entry = ctk.CTkEntry(self.login_frame, width=300)
        self.username_entry.grid(row=1, column=0, padx=20)

        self.register_button = ctk.CTkButton(self.login_frame, text="Register", command=self.register)
        self.register_button.grid(row=2, column=0, padx=20, pady=20)

        self.warning_message = ctk.CTkLabel(self.login_frame)
    
    def register(self):
        username = self.username_entry.get()
        
        res = self.proxy.register(username)
        self.user = username
        # if "NO" in res:
        #     self.login_label.configure(text=f"{username} already exists. Please choose another.", text_color="red")
        # else:
        self.switch_screen(self.login_frame, ChatRoom)