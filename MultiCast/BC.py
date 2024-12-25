import socket
import struct
import time
from group import JoinGroup

BR_HOST = '127.0.0.1'  # BR server address
BR_TCP_PORT = 7777
MULTICAST_GROUP_C = '225.6.7.8'
MULTICAST_PORT = 8888

BUFFER_SIZE = 1024

def create_udp():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, struct.pack('b', 1))
    JoinGroup(udp_sock, MULTICAST_GROUP_C, True)
    return udp_sock

def send_to_multicast_group(data, udp_sock):
    udp_sock.sendto(data, (MULTICAST_GROUP_C, MULTICAST_PORT))
    print(f"BC rebroadcasted to multicast group {MULTICAST_GROUP_C}:{MULTICAST_PORT}")

def bc_client():
    udp_sock = create_udp()
    tcp_sock = None

    try:
        while True:
            if tcp_sock is None or tcp_sock.fileno() == -1:
                if tcp_sock:
                    tcp_sock.close()
                tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    tcp_sock.connect((BR_HOST, BR_TCP_PORT))
                    print(f"BC connected to BR at {BR_HOST}:{BR_TCP_PORT}")
                except socket.error as e:
                    print(f"Failed to connect to BR: {e}")
                    time.sleep(5)
                    continue
            try:
                while True:
                    data = tcp_sock.recv(BUFFER_SIZE)
                    if not data:  # 檢測伺服器關閉連線
                        print("Connection closed by BR, reconnecting...")
                        tcp_sock.close()
                        tcp_sock = None
                        break

                    print(f"BC received message: {data.decode('utf-8')}")
                    send_to_multicast_group(data, udp_sock)

            except (socket.error, ConnectionResetError) as e:
                print(f"Connection error: {e}. Reconnecting...")
                tcp_sock.close()
                tcp_sock = None 
                break

    except KeyboardInterrupt:
        print("KeyboardInterrupt detected. Exiting...")
    finally:
        # 清理資源
        if tcp_sock:
            tcp_sock.close()
        JoinGroup(udp_sock, MULTICAST_GROUP_C, False)
        udp_sock.close()
        print("Resources cleaned up. Bye!")


if __name__ == '__main__':
    bc_client()
