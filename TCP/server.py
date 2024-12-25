import socket, threading, random, time

PORT = 8888
BACKLOG = 5
BUF_SIZE = 1024

class ServerThread(threading.Thread):
    def __init__(self, t_name, client_sc, rip, rport):
        super().__init__(name = t_name)
        self.client = client_sc
        self.rip = rip
        self.rport = rport
        self.start()
    
    def run(self):
        name = threading.current_thread().name
        while True:
            data = self.client.recv(BUF_SIZE).decode()
            if not data or int(data) <= 0:
                print("Number is 0, closing connection.")
                break
            
            number = int(data)
            print(f"Thread {name} received number: {number}")
            number -= 1
            
            time.sleep(1)
            self.client.sendall(str(number).encode())

        self.client.close()
        print(name, 'Thread closed')


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print('Starting up server on port: %s' % (PORT))
    server_socket.bind(('', PORT))
    server_socket.listen(BACKLOG)

    while True:
        client, (rip, rport) = server_socket.accept()
        print("Receive messgae from IP: " + str(rip) + " port: " + str(rport))
        thread = ServerThread(random.randint(1, 100), client, rip, rport)

if __name__ == '__main__':
    main()