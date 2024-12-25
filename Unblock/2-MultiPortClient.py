####################################################
#  Network Programming - Unit 8 Non-blocking Socket         
#  Program Name: 2-MultiPortClient.py                                      			
#  The program is a simple non-blocking TCP server.            		
#  2021.08.02                                                  									
####################################################import sys
import sys
import socket

BUF_SIZE = 1024

def main():
	if(len(sys.argv) < 3):
		print("Usage: python3 2-MultiPortClient.py ServerIP port [message]\n")
		exit(1)

	# Get server IP
	serverIP = socket.gethostbyname(sys.argv[1])
	port = int(sys.argv[2])
	
	# Create a TCP client socket
	cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect to server
	cSocket.connect((serverIP, port))
	
	# Send message to server
	if(len(sys.argv) > 3):
		msg = sys.argv[3]
	else:
		msg = "Client hello!!"
	cSocket.send(msg.encode('utf-8'))
	
	# Receive server reply, buffer size = 1024
	server_reply = cSocket.recv(BUF_SIZE)
	print(server_reply.decode('utf-8'))
	
	# Close the TCP socket
	cSocket.close()

# end of main


if __name__ == '__main__':
	main()
