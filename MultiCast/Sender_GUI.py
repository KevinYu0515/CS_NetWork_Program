import sys
import socket
import struct
import time
import threading
import customtkinter as ctk
from group import JoinGroup

# 設置初始參數
MULTICAST_GROUP_S = '225.3.2.1'
PORT = 6666
BUFF_SIZE = 1024  # 緩衝區大小

class MulticastSenderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Multicast Sender")
        self.geometry("500x400")
        
        # 多播相關變量
        self.sock = None
        self.running = False
        
        # 設置主界面
        self.group_label = ctk.CTkLabel(self, text="Multicast Group:")
        self.group_label.pack(pady=(20, 5))
        
        self.group_entry = ctk.CTkEntry(self, placeholder_text="Enter group address", width=300)
        self.group_entry.pack(pady=5)
        self.group_entry.insert(0, MULTICAST_GROUP_S)
        
        self.message_label = ctk.CTkLabel(self, text="Message:")
        self.message_label.pack(pady=(20, 5))
        
        self.message_entry = ctk.CTkEntry(self, placeholder_text="Enter message", width=300)
        self.message_entry.pack(pady=5)
        self.message_entry.insert(0, "Hello!!")
        
        self.start_button = ctk.CTkButton(self, text="Start Sending", command=self.start_sending)
        self.start_button.pack(pady=(20, 10))
        
        self.stop_button = ctk.CTkButton(self, text="Stop Sending", command=self.stop_sending, state="disabled")
        self.stop_button.pack(pady=5)
        
        self.output_text = ctk.CTkTextbox(self, width=400, height=150)
        self.output_text.pack(pady=(20, 10), fill="both", expand=True)
    
    def start_sending(self):
        group = self.group_entry.get()
        message = self.message_entry.get()
        
        if not group or not message:
            self.log_output("Error: Multicast group and message cannot be empty.")
            return
        
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.running = True
        
        # 開啟新線程來發送消息
        threading.Thread(target=self.send_multicast, args=(group, PORT, message), daemon=True).start()
    
    def stop_sending(self):
        self.running = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.log_output("Stopped sending multicast messages.")
    
    def send_multicast(self, group, port, message):
        try:
            # 建立多播 socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            JoinGroup(self.sock, group, True)
            self.sock.settimeout(0.2)
            
            ttl = struct.pack('b', 3)
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
            
            group_address = (group, port)
            self.log_output(f"Sending to {group}:{port}")
            
            while self.running:
                self.sock.sendto(message.encode('utf-8'), group_address)
                self.log_output(f"Sent: {message}")
                
                # 接收回應
                try:
                    data, (rip, rport) = self.sock.recvfrom(BUFF_SIZE)
                    self.log_output(f"Received: {data.decode('utf-8')} from {rip}:{rport}")
                except socket.timeout:
                    self.log_output("No response (timeout)")
                
                time.sleep(3)
        
        except Exception as e:
            self.log_output(f"Error: {e}")
        finally:
            if self.sock:
                JoinGroup(self.sock, group, False)
                self.sock.close()
            self.sock = None
            self.log_output("Socket closed.")
    
    def log_output(self, message):
        self.output_text.insert("end", message + "\n")
        self.output_text.yview("end")  # 自動滾動到底部


if __name__ == '__main__':
    app = MulticastSenderApp()
    app.mainloop()
