import socket, sys

PORT = 8888
BUF_SIZE = 1024

def main():
    if(len(sys.argv) < 2):
        print("Usage: python3 client.py ServerIP")
        exit(1)

    serverIP = socket.gethostbyname(sys.argv[1])
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Connecting to %s port %s' % (serverIP, PORT))
    client_socket.connect((serverIP, PORT))

    val = input('Input a integer: ')
    client_socket.sendall(val.encode())

    while True:
        data = client_socket.recv(BUF_SIZE).decode()
        if not data or int(data) <= 0:
            print('Number is 0, closing connection.')
            break

        number = int(data)
        print('Recevied number: %d' % number)

        number -= 1
        client_socket.sendall(str(number).encode()) 

    client_socket.close()

if __name__ == '__main__':
    main()