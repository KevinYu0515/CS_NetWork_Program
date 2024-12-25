from . import App
import customtkinter as ctk
from .mail import Mail
import os
from dotenv import load_dotenv
load_dotenv()

class Login(App):
    def __init__(self, root, socket):
        super().__init__(root=root, user=None, client_socket=socket)
        self.root = root
        self.width = int(os.getenv("LOGIN_WIDTH"))
        self.height = int(os.getenv("LOGIN_HEIGHT"))

        # login root grid
        self.root.geometry(f"{self.width}x{self.height}")
        self.center_window(self.root, self.width, self.height) 
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # login frame
        self.login_frame = ctk.CTkFrame(self.root, width=240, height=200, corner_radius=10)
        self.login_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.login_label = ctk.CTkLabel(self.login_frame, text="Enter your username and password")
        self.login_label.grid(row=0, column=0, pady=(20, 0))

        self.username_entry = ctk.CTkEntry(self.login_frame, width=300, placeholder_text='Username')
        self.username_entry.grid(row=1, column=0, padx=20, pady=(0, 10))

        self.password_entry = ctk.CTkEntry(self.login_frame, width=300, placeholder_text='Password', show="*")
        self.password_entry.grid(row=2, column=0, padx=20)

        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=3, column=0, padx=20, pady=20)

        self.warning_message = ctk.CTkLabel(self.login_frame)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            self.send_and_recevie(f'USER {username}')
            self.send_and_recevie(f'PASS {password}')
            self.user = username
            self.switch_screen(self.login_frame, Mail(root=self.root, user=self.user, socket=self.socket))
        except Exception as e:
            self.login_label.configure(text=f"wrong Username or Password. Please try again.", text_color="red")
            print(e)
            