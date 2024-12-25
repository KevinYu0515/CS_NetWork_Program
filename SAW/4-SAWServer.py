####################################################
#  Network Programming - Unit 5  User Datagram Protocol          
#  Program Name: 4-SAWServer.py                                      			
#  This program builds a server based on SAWSocket.           		
#  2021.07.21                                                 									
####################################################
import SAWSocket, sys

PORT = 8888
BUF_Size = 1024

def main():
	# Create a SAWSocket Server 
	slide_window = 4
	if len(sys.argv) >= 2:
		slide_window = int(sys.argv[1])
	
	server = SAWSocket.SAWSocket(8888, slide_window=slide_window)		# Listen on port 8888
	server.accept()
	
	for i in range(10000):
		msg = server.receive()
		if msg is not None:
			print('Receive message: ' + msg.decode('utf-8'))
	
	server.close()
# end of main

if __name__ == '__main__':
	main()
