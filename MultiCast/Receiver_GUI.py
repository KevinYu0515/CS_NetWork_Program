import socket
import threading
import customtkinter as ctk
from group import JoinGroup

# 設定多播參數
MULTICAST_GROUP2 = '225.6.7.8'
PORT = 8888
BUFF_SIZE = 1024  # 緩衝區大小


class MulticastReceiverApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Multicast Receiver")
        self.geometry("600x400")

        # GUI 元素
        self.group_label = ctk.CTkLabel(self, text="Multicast Group:")
        self.group_label.pack(pady=(20, 5))

        self.group_entry = ctk.CTkEntry(self, placeholder_text="Enter multicast group address", width=400)
        self.group_entry.pack(pady=5)
        self.group_entry.insert(0, MULTICAST_GROUP2)

        self.port_label = ctk.CTkLabel(self, text="Port:")
        self.port_label.pack(pady=(20, 5))

        self.port_entry = ctk.CTkEntry(self, placeholder_text="Enter port", width=100)
        self.port_entry.pack(pady=5)
        self.port_entry.insert(0, str(PORT))

        self.start_button = ctk.CTkButton(self, text="Start Listening", command=self.start_listening)
        self.start_button.pack(pady=(20, 10))

        self.stop_button = ctk.CTkButton(self, text="Stop Listening", command=self.stop_listening, state="disabled")
        self.stop_button.pack(pady=5)

        self.output_text = ctk.CTkTextbox(self, width=500, height=200)
        self.output_text.pack(pady=(20, 10), fill="both", expand=True)

        # 多播相關變量
        self.recv_socket = None
        self.running = False

    def start_listening(self):
        group = self.group_entry.get()
        port = self.port_entry.get()

        if not group or not port.isdigit():
            self.log_output("Error: Invalid multicast group or port.")
            return

        port = int(port)

        # 啟動監聽線程
        self.running = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        threading.Thread(target=self.listen_multicast, args=(group, port), daemon=True).start()

    def stop_listening(self):
        self.running = False
        if self.recv_socket:
            self.recv_socket.close()
            self.recv_socket = None
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.log_output("Stopped listening to multicast group.")

    def listen_multicast(self, group, port):
        try:
            # 創建多播 socket
            self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.recv_socket.bind(('', port))

            # 加入多播群組
            JoinGroup(self.recv_socket, group, True)
            self.log_output(f"Listening on multicast group ({group}, {port})")

            while self.running:
                try:
                    # 接收多播消息
                    data, (rip, rport) = self.recv_socket.recvfrom(BUFF_SIZE)
                    msg = f"Received message: {data.decode('utf-8')} from {rip}:{rport}"
                    self.log_output(msg)
                except socket.error as e:
                    self.log_output(f"Socket error: {e}")
        except Exception as e:
            self.log_output(f"Error: {e}")
        finally:
            if self.recv_socket:
                JoinGroup(self.recv_socket, group, False)
                self.recv_socket.close()
            self.recv_socket = None
            self.log_output("Socket closed.")

    def log_output(self, message):
        self.output_text.insert("end", message + "\n")
        self.output_text.yview("end")  # 自動滾動到底部


if __name__ == '__main__':
    app = MulticastReceiverApp()
    app.mainloop()
