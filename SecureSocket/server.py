# D1149371 林鈺凱 資訊三甲

import socket, threading, random, time, ssl

PORT = 8888
BACKLOG = 5
BUF_SIZE = 1024
SERVER_CERT = './server.cer'
SERVER_KEY = './server.key'
CLIENT_CERT = './client2.cer'

class ServerThread(threading.Thread):
    def __init__(self, t_name, client_sc, rip, rport):
        super().__init__(name = t_name)
        self.client = client_sc
        self.rip = rip
        self.rport = rport
        self.start()

        self.client.settimeout(10)
    
    def run(self):
        name = threading.current_thread().name
        while True:
            try:
                data = self.client.recv(BUF_SIZE).decode()
                if not data or int(data) <= 0:
                    print("Number is 0, closing connection.")
                    break
                
                number = int(data)
                print(f"Thread {name} received number: {number}")
                number -= 1
                
                time.sleep(1)
                self.client.sendall(str(number).encode())
            except socket.timeout:
                print(f"Connection with {self.rip}:{self.rport} timed out.")
                break

        self.client.close()
        print(name, 'Thread closed')


def main():
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # ctx.verify_mode = ssl.CERT_REQUIRED
    ctx.load_cert_chain(certfile=SERVER_CERT, keyfile=SERVER_KEY)
    # ctx.load_verify_locations(cafile=CLIENT_CERT)

    print('Starting up server on port: %s' % (PORT))
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', PORT))
    server_socket.listen(BACKLOG)

    while True:
        client, (rip, rport) = server_socket.accept()
        ssl_conn = ctx.wrap_socket(client, server_side=True)
        print("Receive messgae from IP: " + str(rip) + " port: " + str(rport))
        thread = ServerThread(random.randint(1, 100), ssl_conn, rip, rport)

if __name__ == '__main__':
    main()