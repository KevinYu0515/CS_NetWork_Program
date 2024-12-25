####################################################
#  Network Programming - Unit 5  User Datagram Protocol          
#  Program Name: 2-UDPClient.py                                      			
#  This program sends 100 UDP messages.           		
#  2021.07.15                                                  									
####################################################
import sys
import socket
import struct
import binascii

PORT = 8888
BUF_Size = 1024

def main():
	if(len(sys.argv) < 2):
		print("Usage: python3 1-UDPClient.py ServerIP\n")
		exit(1)

	# Get server IP
	serverIP = socket.gethostbyname(sys.argv[1])
	
	# Create a UDP client socket
	dgramSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	
	s = struct.Struct('!' + 'I 15s')			# !: network orger
	# Send 100 message
	for i in range(10000):
		msg = 'The %3d message' % i
		record = (i, msg.encode('utf-8'))
		packed_data = s.pack(*record)
		print(msg)
		dgramSocket.sendto(packed_data, (serverIP, PORT))
	
	# Close the UDP socket
	dgramSocket.close()
# end of main

if __name__ == '__main__':
	main()
