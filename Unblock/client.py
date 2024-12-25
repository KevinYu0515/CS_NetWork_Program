import socket, time, sys

def producer():
    server_host = "127.0.0.1"
    server_port = 8880

    while True:
        data = input("Enter an integer to send to server (or 'exit' to quit): ")
        if data.lower() == "exit":
            break

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((server_host, server_port))
            sock.sendall(data.encode())
            response = sock.recv(1024).decode()
            print(f"Server response: {response}")


def consumer():
    server_host = "127.0.0.1"
    server_port = 8881

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((server_host, server_port))
        while True:
            sock.sendall(b"Request data")
            response = sock.recv(1024).decode()
            if response == "Waiting for data...":
                print("資料等待中...")
                time.sleep(2)
            else:
                print(f"Received data: {response}")
                break

if __name__ == '__main__':
    if(len(sys.argv) == 3):
        worker = sys.argv[-1]
        if worker == 'producer':
            producer()
        elif worker == 'consumer':
            consumer()