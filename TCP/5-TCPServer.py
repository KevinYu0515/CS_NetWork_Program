####################################################
#  Network Programming - Unit 2 Simple TCP Client Server Program         
#  Program Name: 5-TCPServer.py                                      			
#  The program is a simple TCP server. The program receive a structure of data.           		
#  2021.07.13                                                   									
####################################################
import socket
import struct
import binascii

PORT = 6666
backlog = 5
BUF_SIZE = 1024			# Receive buffer size

def main():
	# Create a TCP Server socket
	srvSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Enable reuse address/port
	srvSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	# Bind 	on any incoming interface with PORT, '' is any interface
	print('Starting up server on port: %s' % (PORT))
	srvSocket.bind(('', PORT))
	
	# Listen incomming connection, connection number = backlog (5)
	srvSocket.listen(backlog)
	
	# Accept the incomming connection
	print('Waiting to receive message from client')
	client, (rip, rport) = srvSocket.accept()
	
	# Receive client message, buffer size = BUF_SIZE
	client_msg = client.recv(BUF_SIZE)
	if client_msg:
		msg = "Receive messgae from IP: " + str(rip) + " port: " + str(rport)
		print(msg)
		print('Received value : ', binascii.hexlify(client_msg))
		# Unpack data
		s = struct.Struct('!' + 'I 10s f')							# ! is network order (receive format is network order)
		unpacked_data = s.unpack(client_msg)
		print('The data you receive:\n Integer=%d\n String=%s\n Floating point=%f\n' %(unpacked_data[0], unpacked_data[1].decode('utf-8'), unpacked_data[2]))

	client.close()
	# Close the TCP socket
	srvSocket.close()
# end of main

if __name__ == '__main__':
	main()
