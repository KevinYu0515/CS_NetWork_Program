####################################################
#  Network Programming - Unit 5  User Datagram Protocol          
#  Program Name: 2-UDPServer.py                                      			
#  This program receives 100 UDP messages.           		
#  2021.07.15                                                  									
####################################################
import socket
import struct
import binascii
import time

PORT = 8888
BUF_Size = 1024

def main():
	# Create a UDP Server socket
	dgramSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	# Bind 	on any incoming interface with PORT, '' is any interface
	dgramSocket.bind(('', PORT))

	print('Waiting on port: %s ' % PORT)
	
	# Receive client message
	s = struct.Struct('!' + 'I 15s')			# !: network orger
	i = 0
	while True:
		recv_data, (rip, rport) = dgramSocket.recvfrom(BUF_Size)
		unpacked_data = s.unpack(recv_data)
		n = unpacked_data[0]
		msg = unpacked_data[1].decode('utf-8')
		print('%d : Receive %dth message: (%s) from %s:%s' % (i, n, msg, str(rip), str(rport)))
		i += 1

	# Close the UDP socket
	dgramSocket.close()
# end of main

if __name__ == '__main__':
	main()
