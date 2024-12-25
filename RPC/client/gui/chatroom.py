from . import App
import customtkinter as ctk
from .create import Create
from .subject import Subject
from PIL import Image
import os

image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
       
class ChatRoom(App):
    def __init__(self, root, user):
        super().__init__(root, user)
        self.subject_id = None
        self.subject = None
        self.subject_message = {}
        self.delete_image = ctk.CTkImage(Image.open(os.path.join(image_path, "trash.png")), size=(26, 26))

        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(3, weight=0)
        self.main_frame.grid_columnconfigure((1, 2), weight=3)
        self.main_frame.grid_rowconfigure((0, 1, 2), weight=1)
        self.sidebar_item = []
        self.sidebar_item_text = []

        # sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self.main_frame, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsw")

        self.create_btn = ctk.CTkButton(self.sidebar_frame, fg_color="transparent", text="CREATE", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.pop_create_dialog)
        self.create_btn.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

        self.subject_btn = ctk.CTkButton(self.sidebar_frame, fg_color="transparent", text="SUBJECT", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.pop_subject_dialog)
        self.subject_btn.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew")

        self.subject_frame = ctk.CTkFrame(self.sidebar_frame)
        self.subject_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.subject_frame_label = ctk.CTkLabel(self.subject_frame, text="")
        self.subject_frame_label.grid(row=0, column=0, padx=10, pady=20, sticky="nsew")

        self.delete_subject_btn = ctk.CTkButton(self.sidebar_frame, fg_color="transparent", text="DELETE", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.delete_subject)
        self.delete_subject_btn.grid_forget()

        # main frame
        self.textbox = ctk.CTkScrollableFrame(self.main_frame, width=250, fg_color="#1d1e1e")
        self.textbox.grid(row=0, column=1, rowspan=3, columnspan=3, padx=20, pady=(20, 0), sticky="nsew")
        self.textbox.columnconfigure((0, 1), weight=1)

        self.entry = ctk.CTkEntry(self.main_frame, placeholder_text="Enter Your Reply")
        self.entry.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.submit = ctk.CTkButton(self.main_frame, fg_color="transparent", border_width=2, text="SUBMIT", text_color=("gray10", "#DCE4EE"), command=self.reply_submit)
        self.submit.grid(row=3, column=3, padx=(0, 20), pady=10, sticky="nsew")

        self.subject_btn.bind("<Enter>", self.on_hover)
        self.subject_btn.bind("<Leave>", self.on_leave)
        self.submit.bind("<Enter>", self.on_hover)
        self.submit.bind("<Leave>", self.on_leave)

    def pop_create_dialog(self):
        Create(self.main_frame, self.user)
    
    def pop_subject_dialog(self):
        Subject(self.main_frame, self.user, self.subject, self.discussion)
            
    def reply_submit(self):
        msg = self.entry.get()
        self.entry.delete(0, ctk.END)
        if self.subject is None:
            print("Please Choose A Subject From Left Sidebar")
        else:
            self.proxy.reply(self.subject, msg, self.user)
            self.discussion(self.subject_id, self.subject)

    def discussion(self, id, subject):
        self.subject_id = id
        self.subject = subject
        self.textbox._parent_canvas.yview_moveto(0)
        self.subject_message = {}
        for widget in self.textbox.winfo_children():
            widget.destroy()

        if subject is None:
            self.subject_frame_label.configure(text="")
            self.delete_subject_btn.grid_forget()
            return
        
        self.subject_frame_label.configure(text=subject)
        
        response = self.proxy.discussion(subject)
        for index, (id, username, message, created_time) in enumerate(response):
            msg_box = ctk.CTkFrame(self.textbox, fg_color="transparent")
            msg_box.grid(row=index, column=0, pady=(10, 0), padx=(10, 0), sticky="nsew")
    
            if len(self.subject_message) == 0:
               msg_box.grid_configure(pady=(15, 0))
            if self.user == username:
                msg_box.columnconfigure((1, 2, 3), weight=1)
                msg_box.grid_configure(column=1)
            else:
                msg_box.columnconfigure((0, 1, 2), weight=1)
 
            msg = ctk.CTkLabel(msg_box, text=f"{username}：{message}", anchor="w", fg_color="#029cff", corner_radius=10)
            msg.grid(row=0, column=0, columnspan=4, sticky="nsew")

            msg_detail = ctk.CTkLabel(msg_box, text=created_time, font=ctk.CTkFont(size=10), anchor="w")
            msg_detail.grid(row=1, column=0)

            if self.user == username:
                self.delete_msg_btn = ctk.CTkButton(msg_box, width=10, text="", fg_color="#343638", compound="left", border_spacing=0, image=self.delete_image, command=lambda id=id: self.delete_msg(id))
                self.delete_msg_btn.grid(row=0, column=0, padx=5)
                msg.grid(column=1, columnspan=3)
                msg_detail.grid(row=1, column=0, columnspan=3)
                
                self.delete_msg_btn.bind("<Enter>", self.on_hover)
                self.delete_msg_btn.bind("<Leave>", self.on_leave)

            self.subject_message[id] = msg_box
            print(len(self.subject_message))

        if not self.proxy.check_subject(self.subject_id, self.user) or len(self.subject_message) > 0:
            self.delete_subject_btn.grid_forget()
        else:
            self.delete_subject_btn.grid(row=3, column=0, padx=10, pady=(5, 0), sticky="nsew")

    def delete_msg(self, id):
        self.proxy.delete_msg(id)
        self.subject_message[id].destroy()
        self.subject_message.pop(id, None)
        self.discussion(self.subject_id, self.subject)

    def delete_subject(self):
        response = self.proxy.delete(self.subject_id)
        if "Failed" in response:
            print("請確認所有訊息已刪除，才可刪除此主題")
            self.discussion(self.subject_id, self.subject)
            return
        self.discussion(None, None)
    