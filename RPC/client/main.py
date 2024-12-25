import customtkinter as ctk
from gui.login import Login 

if __name__ == '__main__':
    root = ctk.CTk()
    app = Login(root)
    root.mainloop()