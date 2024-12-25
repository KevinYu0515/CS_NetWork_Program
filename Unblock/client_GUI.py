import customtkinter as ctk
import socket
import threading
import time

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Producer-Consumer GUI")
        self.geometry("500x400")

        # Role selection
        self.role_label = ctk.CTkLabel(self, text="Select Role:")
        self.role_label.pack(pady=10)

        # Create a frame to hold radio buttons for alignment
        self.role_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.role_frame.pack(pady=10)

        self.role_var = ctk.StringVar(value="producer")
        self.producer_button = ctk.CTkRadioButton(
            self.role_frame,
            text="Producer",
            variable=self.role_var, 
            value="producer", 
            command=self.toggle_input
        )
        self.producer_button.grid(row=0, column=0, padx=10)

        self.consumer_button = ctk.CTkRadioButton(
            self.role_frame, 
            text="Consumer", 
            variable=self.role_var, 
            value="consumer", 
            command=self.toggle_input
        )
        self.consumer_button.grid(row=0, column=1, padx=10)

        # Input for producer (initially visible)
        self.input_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.input_label = ctk.CTkLabel(self.input_frame, text="Input Data (For Producer):")
        self.input_label.pack(pady=5)

        self.input_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Enter an integer")
        self.input_entry.pack(pady=5)

        self.input_frame.pack(pady=10)  # Initially visible

        # Submit button
        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.start_worker)
        self.submit_button.pack(pady=10)

        # Output area
        self.producer_output_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.producer_output_text = ctk.CTkTextbox(self.producer_output_frame, height=10, width=40)
        self.producer_output_text.pack(padx=10, pady=10, fill="both", expand=True)
        self.producer_output_frame.pack(padx=10, pady=10, fill="both", expand=True)  # Initially visible

        self.consumer_output_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.consumer_output_text = ctk.CTkTextbox(self.consumer_output_frame, height=10, width=40)
        self.consumer_output_text.pack(padx=10, pady=10, fill="both", expand=True)
        self.consumer_output_frame.pack_forget()  # Initially hidden

        # Server configs
        self.server_host = "127.0.0.1"
        self.producer_port = 8880
        self.consumer_port = 8881
        self.cs_running = False

        self.protocol("WM_DELETE_WINDOW", self.on_close) 

    def on_close(self):
        self.cs_running = False
        self.destroy()

    def log(self, role, message):
        if role == "producer":
            self.producer_output_text.insert("end", message + "\n")
            self.producer_output_text.see("end")
        elif role == "consumer":
            self.consumer_output_text.insert("end", message + "\n")
            self.consumer_output_text.see("end")

    def toggle_input(self):
        role = self.role_var.get()
        if role == "producer":
            self.input_frame.pack(pady=10, before=self.submit_button)  # Show input frame
            self.producer_output_frame.pack(padx=10, pady=10, fill="both", expand=True)  # Show producer output
            self.consumer_output_frame.pack_forget()
        elif role == "consumer":
            self.input_frame.pack_forget()  # Hide input frame
            self.consumer_output_frame.pack(padx=10, pady=10, fill="both", expand=True)  # Show consumer output
            self.producer_output_frame.pack_forget()

    def start_worker(self):
        role = self.role_var.get()
        if role == "producer":
            data = self.input_entry.get()
            if data.strip():
                threading.Thread(target=self.producer, args=(data,)).start()
        elif role == "consumer":
            threading.Thread(target=self.consumer).start()

    def producer(self, data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect((self.server_host, self.producer_port))
                sock.sendall(data.encode())
                response = sock.recv(1024).decode()
                self.log("producer", f"Server response: {response}")
                self.input_entry.delete(0, 'end')
            except Exception as e:
                self.log("producer", f"Producer error: {e}")

    def consumer(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            self.cs_running = True
            try:
                sock.connect((self.server_host, self.consumer_port))
                while self.cs_running:
                    sock.sendall(b"Request data")
                    response = sock.recv(1024).decode()
                    if response == "Waiting for data...":
                        self.log("consumer", "資料等待中...")
                        time.sleep(2)
                    else:
                        self.log("consumer", f"Received data: {response}")
                        break
                sock.close()
            except Exception as e:
                self.log("consumer", f"Consumer error: {e}")

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    app = App()
    app.mainloop()
