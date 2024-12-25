from . import App
import customtkinter as ctk

class Subject(App):
    def __init__(self, root, user, subject, discussion):
        super().__init__(root, user)
        self.subject = subject
        self.subject_item = []
        self.discussion = discussion

        self.subject_dialog = ctk.CTkToplevel(root)
        self.subject_dialog.grid_columnconfigure(0, weight=1)
        self.subject_dialog.grid_rowconfigure(0, weight=1)
        self.subject_dialog.title("List ALL Subject")
        self.subject_dialog.geometry("500x500")
        self.center_window(self.subject_dialog, 500, 500)
        self.subject_dialog.attributes("-topmost", True)

        self.subject_frame = ctk.CTkScrollableFrame(self.subject_dialog)
        self.subject_frame.grid(row=0, column=0, sticky="nsew")
        self.subject_frame.columnconfigure(0, weight=1)

        self.handle_subject()

    def handle_subject(self):
        subjects = self.proxy.subject()
        self.subject_item = []
        for widget in self.subject_frame.winfo_children():
            widget.destroy()

        for index, (id, name, description, created_user, created_time) in enumerate(subjects):
            _frame = ctk.CTkFrame(self.subject_frame, fg_color="#1d1e1e")
            _frame.grid(row=index, column=0, padx=10, pady=5, sticky="nsew")
            if self.subject == name:
                _frame.configure(fg_color="#029cff")

            name_label = ctk.CTkLabel(_frame, text=name, font=ctk.CTkFont(size=15), anchor="w")
            name_label.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="nsew")
            
            description_label = ctk.CTkLabel(_frame, text=description, font=ctk.CTkFont(size=12), anchor="w")
            description_label.grid(row=1, column=0, padx=10, sticky="nsew")

            detial_label = ctk.CTkLabel(_frame, text=f"created：{created_time}｜{created_user}", font=ctk.CTkFont(size=10))
            detial_label.grid(row=2, column=0, padx=10, pady=(5, 0), sticky="nsew")

            _frame.bind("<Button-1>", lambda event, _frame=_frame, id=id, name=name: self.onclick_subject(_frame, id, name))
            _frame.bind("<Enter>", self.on_hover)
            _frame.bind("<Leave>", self.on_leave)

            self.subject_item.append(_frame)

    
    def onclick_subject(self, frame: ctk.CTkFrame, id, subject):
        frame.configure(fg_color="#029cff")
        self.discussion(id, subject)
        self.subject_dialog.destroy()
