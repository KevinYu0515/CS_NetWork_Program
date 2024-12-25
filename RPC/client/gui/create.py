from . import App
import customtkinter as ctk
from dotenv import load_dotenv
load_dotenv()

class Create(App):
    def __init__(self, root, user):
        super().__init__(root, user)
        self.create_dialog = ctk.CTkToplevel(root)
        self.create_dialog.title("Create Item")
        self.create_dialog.geometry("400x400")
        self.center_window(self.create_dialog, 400, 400)
        self.create_dialog.attributes("-topmost", True)
        self.create_dialog.grid_columnconfigure((0, 1, 2), weight=1)
        self.create_dialog.grid_rowconfigure((0, 2, 3), weight=1)

        label = ctk.CTkLabel(self.create_dialog, text="Enter Subject Name And Description")
        label.grid(row=0, column=0, columnspan=3, pady=(5, 0), sticky="nsew")

        label_name = ctk.CTkLabel(self.create_dialog, text="Name", anchor="e")
        label_name.grid(row=1, column=0, padx=(5, 0), pady=(5, 0), sticky="nsew")
        entry_name = ctk.CTkEntry(self.create_dialog)
        entry_name.grid(row=1, column=1, padx=(20, 0), pady=10, sticky="nsew")

        label_description = ctk.CTkLabel(self.create_dialog, text="Description", anchor="ne")
        label_description.grid(row=2, column=0, padx=(5, 0), pady=(5, 0), sticky="nsew")
        entry_description = ctk.CTkTextbox(self.create_dialog)
        entry_description.grid(row=2, column=1, padx=(20, 0), pady=(0, 5), sticky="nsew")

        submit_button = ctk.CTkButton(self.create_dialog, width=200, text="Submit", command=lambda: self.create_subject(entry_name.get(), entry_description.get("1.0", ctk.END)))
        submit_button.grid(row=3, column=0, columnspan=3, pady=5)

    def create_subject(self, name, description):
        self.proxy.create(name, description, self.user)
        self.create_dialog.destroy()