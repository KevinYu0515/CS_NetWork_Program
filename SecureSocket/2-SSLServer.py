####################################################
#  Network Programming - Unit 6 Secure Socket         
#  Program Name: 2-SSLServer.py                                      			
#  The program verify the client certificate.            		
#  2021.07.28                                                 									
####################################################
import socket
import ssl

PORT = 6666
backlog = 5
recv_buff_size = 1024			# Receive buffer size
SERVER_CERT = './Openssl/server.cer'
SERVER_KEY = './Openssl/server.key'
CLIENT_CERT = './Openssl/client2.cer'


def main():
	# Create  context & Load Certificate
	ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
	ctx.verify_mode = ssl.CERT_REQUIRED
	ctx.load_cert_chain(certfile=SERVER_CERT, keyfile=SERVER_KEY)
	ctx.load_verify_locations(cafile=CLIENT_CERT)
	
	# Create a TCP Server socket
	srvSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	srvSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	srvSocket.bind(('', PORT))
	srvSocket.listen(backlog)
	
	while True:
		try:
			print('Waiting for client...')
			client, (rip, rport) = srvSocket.accept()
			print('Client connect from %s:%s' % (str(rip), str(rport)))
			ssl_conn = ctx.wrap_socket(client, server_side=True)
			print('SSL established. Peer certificate: '  + str(ssl_conn.getpeercert()))
			print('Cipher be used:' + str(ssl_conn.cipher()))
			client_msg = ssl_conn.recv(recv_buff_size)
			while client_msg:
				msg = "Receive messgae: " + client_msg.decode('utf-8')
				print(msg)
				client_msg = ssl_conn.recv(recv_buff_size)
			print('Close connection')
			ssl_conn.close()
			print('===')
		except KeyboardInterrupt:
			print('Server exit!!')
			break
		except:
			print('SSL error')
	srvSocket.close()
# end of main

if __name__ == '__main__':
	main()
