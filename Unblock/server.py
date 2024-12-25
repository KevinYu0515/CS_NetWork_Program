import socket
import threading
import queue
import time

class ServerThread(threading.Thread):
    def __init__(self, host, port, queue, role):
        super().__init__()
        self.host = host
        self.port = port
        self.queue = queue
        self.role = role
        self.running = True

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            print(f"{self.role.capitalize()} server running on port {self.port}...")

            while self.running:
                conn, addr = server_socket.accept()
                print(f"Connection from {addr}")
                if self.role == "producer":
                    threading.Thread(target=self.handle_producer, args=(conn,)).start()
                elif self.role == "consumer":
                    threading.Thread(target=self.handle_consumer, args=(conn,)).start()

    def handle_producer(self, conn):
        try:
            data = conn.recv(1024).decode()
            if not data:
                return
            try:
                num = int(data)
                if self.queue.full():
                    conn.sendall(b"Error: Queue is full.")
                else:
                    self.queue.put(num)
                    conn.sendall(b"Success: Added to queue.")
            except ValueError:
                conn.sendall(b"Error: Invalid input.")
        except Exception as e:
            print(e)
        finally:
            tmp = []
            while not self.queue.empty():
                tmp.append(self.queue.get())
            print(tmp)
            for i in tmp:
                self.queue.put(i)
            conn.close()

    def handle_consumer(self, conn):
        try:
            while True:
                if not self.queue.empty():
                    num = self.queue.get()
                    conn.sendall(f"{num}".encode())
                    break
                else:
                    conn.sendall(b"Waiting for data...")
                    time.sleep(2)
        except Exception as e:
            print(e)
        finally:
            time.sleep(2)
            tmp = []
            while not self.queue.empty():
                tmp.append(self.queue.get())
            print(tmp)
            for i in tmp:
                self.queue.put(i)
            conn.close()

    def stop(self):
        self.running = False

def main():
    shared_queue = queue.Queue(maxsize=5)
    producer_server = ServerThread(host="0.0.0.0", port=8880, queue=shared_queue, role="producer")
    consumer_server = ServerThread(host="0.0.0.0", port=8881, queue=shared_queue, role="consumer")
    producer_server.start()
    consumer_server.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        producer_server.stop()
        consumer_server.stop()
        producer_server.join()
        consumer_server.join()
        print("Servers stopped.")

if __name__ == "__main__":
    main()