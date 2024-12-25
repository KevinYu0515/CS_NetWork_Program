# D1149371 林鈺凱 資訊三甲

import socket, threading, random, struct

PORT = 8888
BACKLOG = 5
BUF_SIZE = 1024

class ServerThread(threading.Thread):
    def __init__(self, t_name, server_socket, recv_data, rip, rport):
        super().__init__(name = t_name)
        self.server_socket = server_socket
        self.recv_data = recv_data
        self.rip = rip
        self.rport = rport
        self.id = 0
        self.start()
    
    def run(self):
        name = threading.current_thread().name
        
        s = struct.Struct('!' + 'I 15s')
        self.id += 1
        unpacked_data = s.unpack(self.recv_data)
        n = unpacked_data[0]
        msg = unpacked_data[1].rstrip(b'\x00').decode()
        print('%d : Receive %dth message: (%s) from %s:%s' % (self.id, n, msg, str(self.rip), str(self.rport)))
        msg = int(msg)
        if msg <= 0:
            print(name, f'Thread {self.name} closed')
        msg -= 1
        self.send(str(msg))
    
    def send(self, number: str):
        s = struct.Struct('!' + 'I 15s')
        self.id += 1
        record = (self.id, number.encode('utf-8'))
        packed_data = s.pack(*record)

        self.server_socket.sendto(packed_data, (self.rip, self.rport))


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print('Starting up server on port: %s' % (PORT))
    server_socket.bind(('', PORT))

    while True:
        recv_data, (rip, rport) = server_socket.recvfrom(BUF_SIZE)
        print("Receive messgae from IP: " + str(rip) + " port: " + str(rport))
        thread = ServerThread(random.randint(1, 100), server_socket, recv_data, rip, rport)

if __name__ == '__main__':
    main()