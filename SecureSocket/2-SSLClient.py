####################################################
#  Network Programming - Unit 6 Secure Socket          
#  Program Name: 2-SSLClient.py                                      			
#  The program verify the server certificate.      
#  2021.07.28                                                  									
####################################################
import sys
import socket
import ssl

PORT = 6666
recv_buff_size = 1024			# Receive buffer size
SERVER_CERT = './Openssl/server.cer'
CLIENT_CERT_PATH = './Openssl/'

def main():
	if(len(sys.argv) < 2):
		print("Usage: python3 2-SSLClient.py ServerIP Client_Sertificate")
		exit(1)

	# Get server IP
	serverIP = socket.gethostbyname(sys.argv[1])
	CLIENT_CERT = CLIENT_CERT_PATH + sys.argv[2] + '.cer'
	CLIENT_KEY = CLIENT_CERT_PATH + sys.argv[2] + '.key'
	
	# Verify server Certificate
	ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=SERVER_CERT)
	ctx.load_cert_chain(certfile=CLIENT_CERT, keyfile=CLIENT_KEY)
	
	# Create a TCP client socket
	cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	# Wrap socket
	ssl_conn = ctx.wrap_socket(cSocket, server_side=False, server_hostname=sys.argv[1])
	
	# Connect to server
	print('Connecting to %s port %s' % (serverIP, PORT))
	try:
		ssl_conn.connect((serverIP, PORT))
		print('SSL established. Peer certificate: '  + str(ssl_conn.getpeercert()))
	
		# Send message to server
		msg = "Application data from client!!"
		ssl_conn.send(msg.encode('utf-8'))
	except:
		print('SSL error')
		
	print('Closing connection.')
	# Close the SSL socket
	ssl_conn.close()
# end of main


if __name__ == '__main__':
	main()
