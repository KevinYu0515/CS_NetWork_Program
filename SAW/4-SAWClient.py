####################################################
#  Network Programming - Unit 5  User Datagram Protocol          
#  Program Name: 4-SAWClient.py                                      			
#  This program build a client based on SAWSocket.           		
#  2021.07.21                                             									
####################################################
import SAWSocket
import sys

PORT = 8888
BUF_Size = 1024

def main():
	slide_window = 4
	if(len(sys.argv) < 3):
		print("Usage: python3 3-SAWClient.py ServerIP\n")
		exit(1)

	slide_window = int(sys.argv[2])
	# Create a SAWSocket client 
	client = SAWSocket.SAWSocket(PORT, sys.argv[1], slide_window)
	client.connect()
	
	msgs = []
	for i in range(10000):
		msg = 'Test message ' + str(i) + '\n'
		msgs.append(msg)
		if len(msgs) == slide_window:
			client.send(msgs)
			msgs.clear()

	client.close()

# end of main

if __name__ == '__main__':
	main()
