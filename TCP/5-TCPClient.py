####################################################
#  Network Programming - Unit 2 Simple TCP Client Server Program         
#  Program Name: 5-TCPClient.py                                      			
#  The program is a simple TCP client. The program send a structure of data.           		
#  2021.07.13                                                   									
####################################################
import sys
import socket
import struct
import binascii

PORT = 6666
BUF_SIZE = 1024			# Receive buffer size

def main():
	if(len(sys.argv) < 2):
		print("Usage: python3 5-TCPClient.py ServerIP")
		exit(1)

	in1 = input('Input a integer: ')
	val1 = int(in1)
	in2 = input('Input a string (length < 10): ')
	val2 = in2[0:10]
	in3 = input('Input a floating point: ')
	val3 = float(in3)
	
	print('The data you input:\n Integer=%d\n String=%s\n Floating point=%f\n' %(val1, val2, val3))
	
	# Pack data into network order
	record = (val1, val2.encode('utf-8'), val3)		# must encode a string to bytes
	s = struct.Struct('!' + 'I 10s f')							# ! is network order
	packed_data = s.pack(*record)
	print('Packed value : ', binascii.hexlify(packed_data))
	
	# Get server IP
	serverIP = socket.gethostbyname(sys.argv[1])
	
	# Create a TCP client socket
	cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	# Connect to server
	print('Connecting to %s port %s' % (serverIP, PORT))
	cSocket.connect((serverIP, PORT))
	
	# Send message to server
	try:
		print('Send: %s' % packed_data)
		cSocket.send(packed_data)
	except socket.error as e:
		print('Socket error: %s' % str(e))
	except Exception as e:
		print('Other exception: %s' % str(e))
	finally:
		print('Closing connection.')
		# Close the TCP socket
		cSocket.close()

# end of main


if __name__ == '__main__':
	main()
