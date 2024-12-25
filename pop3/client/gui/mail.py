from . import App
import customtkinter as ctk
import os
from collections import namedtuple
from dotenv import load_dotenv
from email import parser
from email.header import decode_header

load_dotenv()

image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
       
class Mail(App):
    def __init__(self, root, user, socket):
        super().__init__(root, user, client_socket=socket)
        self.subject_id = None
        self.subject = None
        self.width = int(os.getenv("MAIN_WIDTH"))
        self.height = int(os.getenv("MAIN_HEIGHT"))

        self.root.geometry(f"{self.width}x{self.height}")
        self.center_window(self.root, self.width, self.height) 
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=2)
        self.main_frame.grid_columnconfigure((1, 2, 3), weight=10)
        self.main_frame.grid_rowconfigure(0, weight=3)
        self.main_frame.grid_rowconfigure(1, weight=10)
        self.main_frame.grid_rowconfigure(2, weight=10)
        self.main_frame.grid_rowconfigure(3, weight=10)
        self.main_frame.grid_rowconfigure(4, weight=2)
        self.sidebar_item = []
        self.sidebar_item_text = []
        self.delete_email_id = []

        # sidebar frame
        self.sidebar_frame = ctk.CTkScrollableFrame(self.main_frame, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.emails = self.fetch_emails()
        self.spawn_sidebar(self.emails)

        # main frame
        self.email_frame = ctk.CTkFrame(self.main_frame, fg_color="#1d1e1e")
        self.email_frame.grid(row=0, column=1, rowspan=1, columnspan=3, padx=20, pady=(10, 0), sticky="nsew")

        self.email_frame2 = ctk.CTkScrollableFrame(self.main_frame, fg_color="#1d1e1e")
        self.email_frame2.grid(row=1, column=1, rowspan=3, columnspan=3, padx=20, pady=10, sticky="nsew")

        self.buttons_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.buttons_frame.grid(row=4, column=1, rowspan=1, columnspan=3, padx=20, sticky="nsew")

        # Add buttons to buttons_frame
        button1 = ctk.CTkButton(self.buttons_frame, width=50, text="刪除此信件", command=lambda: self.delete_email(self.subject_id))
        button1.grid(row=0, column=0, padx=10)

    def fetch_emails(self):
        Email = namedtuple('Email', ['date', 'subject', 'from_address', 'to_address'])
        emails = []
        for id in range(1, self.get_emails_count() + 1):
            try:
                reply = self.send_and_recevie(f"RETR {id}")
                reply = reply.split(b'\r\n', 1)[1]
                if reply.endswith(b'\r\n.\r\n'):
                    reply = reply[:-5]
                email = parser.BytesParser().parsebytes(reply)
                headers = self.ParseHeader(email)
                emails.append(Email(*headers))
            except Exception as e:
                print(e)
                continue
        return emails

    def spawn_sidebar(self, emails):
        self.sidebar_item = []
        self.sidebar_item_text = []
        for widget in self.sidebar_frame.winfo_children():
            widget.destroy()

        for idx, email in enumerate(emails):
            if idx + 1 in self.delete_email_id:
                continue

            subject_frame = ctk.CTkFrame(self.sidebar_frame)
            subject_frame.grid(row=idx, column=0, padx=10, pady=5, sticky="nsew")
            self.sidebar_item.append(subject_frame)

            subject_frame_label = ctk.CTkLabel(subject_frame, text=email.subject, anchor='w')
            subject_frame_label.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="nsew")
            subject_frame_label2 = ctk.CTkLabel(subject_frame, text=email.from_address, anchor='w')
            subject_frame_label2.grid(row=1, column=0, padx=(10, 0), pady=(0, 5), sticky="nsew")
            self.sidebar_item_text.append((subject_frame_label, subject_frame_label2))

            subject_frame.bind("<Button-1>", lambda event, subject_frame=subject_frame, idx=idx: self.onclick_subject(subject_frame, idx + 1))
            subject_frame_label.bind("<Button-1>", lambda event, subject_frame=subject_frame, idx=idx: self.onclick_subject(subject_frame, idx + 1))
            subject_frame_label2.bind("<Button-1>", lambda event, subject_frame=subject_frame, idx=idx: self.onclick_subject(subject_frame, idx + 1))

    def onclick_subject(self, frame: ctk.CTkFrame, id):
        if self.subject is not None:
            self.subject.configure(fg_color="#2b2b2b")
        frame.configure(fg_color="#029cff")
        self.subject = frame
        self.subject_id = id
        self.show_email(id)
        
    def delete_email(self, id):
        if self.subject_id is None:
            return
        
        reply = self.send_and_recevie(f"DELE {id}")
        for widget in self.email_frame.winfo_children():
            widget.destroy()
        for widget in self.email_frame2.winfo_children():
            widget.destroy()
        self.subject = None
        self.subject_id = None
        self.delete_email_id.append(id)
        self.spawn_sidebar(self.emails)

    def show_email(self, id):
        reply = self.send_and_recevie(f"RETR {id}")
        reply = reply.split(b'\r\n', 1)[1]
        if reply.endswith(b'\r\n.\r\n'):
            reply = reply[:-5]
        email = parser.BytesParser().parsebytes(reply)
        headers = '\n'.join(line for line in self.ParseHeader(email))
        body = self.ParseContent(email)
        for widget in self.email_frame.winfo_children():
            widget.destroy()
        for widget in self.email_frame2.winfo_children():
            widget.destroy()

        header_label = ctk.CTkLabel(self.email_frame, text=f"{headers}", anchor='w', justify='left')
        header_label.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

        content_label = ctk.CTkLabel(self.email_frame2, text=f"{body}", anchor='w', justify='left')
        content_label.grid(row=1, column=0, padx=10, pady=(5, 0), sticky="nsew")

    def get_emails_count(self):
        reply = self.send_and_recevie("LIST").decode()
        lines = reply.splitlines()
        email_count = 0
        for line in lines[1:]:
            if line == '.':
                break
            email_count += 1
        return email_count

    def ParseHeader(self, email):
        headers = []
        INFO = ["Date", "Subject", "From", "To"]
        for info in INFO:
            if email[info] is not None:
                header, encoding = decode_header(email[info])[0]
                if encoding is not None:
                    headers.append(header.decode(encoding))
                else:
                    headers.append(f"{info}:{header}")
        return headers

    def ParseContent(self, email):
        content_type = email.get_content_type()
        if content_type == "text/plain":
            payload = email.get_payload(decode=True)
            charset = email.get_content_charset()
            if charset is not None:
                return payload.decode(charset)
            return payload