import socket
import struct
import threading
import time
from group import JoinGroup

MULTICAST_GROUP_S = '225.3.2.1'
MULTICAST_PORT = 6666
TCP_PORT = 7777
BUFFER_SIZE = 1024

def handle_bc_connection(conn, addr, multicast_data):
    print(f"BC connected from {addr}")
    try:
        time.sleep(3)
        d = {}
        for data in multicast_data:
            d[data] = d.get(data, 0) + 1
        s = ""
        for data, count in d.items():
            s += f"| {data.decode('utf-8')} [{count}] "
        s += "|"
        conn.sendall(s.encode('utf-8'))

    except Exception as e:
        print(e)
    finally:
        conn.close()
    

def br_server(multicast_data):
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.bind(('', TCP_PORT))
    tcp_sock.listen(5)
    print(f"BR server listening on TCP port {TCP_PORT}")
    
    while True:
        try:
            conn, addr = tcp_sock.accept()
            threading.Thread(target=handle_bc_connection, args=(conn, addr, multicast_data)).start()
        except KeyboardInterrupt:
            print('KeyboardInterrupt')
            break

    tcp_sock.close()

def br_multicast_listener(multicast_data):
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_sock.bind(('', MULTICAST_PORT))
    JoinGroup(udp_sock, MULTICAST_GROUP_S, True)
    print(f"BR listening on multicast group {MULTICAST_GROUP_S}:{MULTICAST_PORT}")
    
    while True:
        try:
            data, _ = udp_sock.recvfrom(BUFFER_SIZE)
            print(f"BR received multicast message: {data.decode('utf-8')}")
            multicast_data.append(data)
        except KeyboardInterrupt:
            print('KeyboardInterrupt')
            break
    
    JoinGroup(udp_sock, MULTICAST_GROUP_S, False)
    udp_sock.close()
            

if __name__ == '__main__':
    multicast_data = []
    threading.Thread(target=br_server, args=(multicast_data,)).start()
    br_multicast_listener(multicast_data)
