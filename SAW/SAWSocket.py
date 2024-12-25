####################################################
#  Network Programming - Unit 5  User Datagram Protocol          
#  Program Name: SAWSocket.py                                      			
#  This program implements stop and wait protocol based on UDP.          		
#  2021.07.19                                                 									
####################################################
import socket
import threading
import time
import struct
import collections

import random

BufSize = 1024
DEBUG = True

class SAWSocket:
	def __init__(self,  port, addr = '', slide_window = 4):			# addr == '' if server
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		if(addr == ''):		# Server side
			self.isServer = True
			self.PeerAddr = ''
			self.PeerPort = 0
			self.slide_window = slide_window
			# Bind 	on any incoming interface with port, '' is any interface
			self.socket.bind(('', port))
		else:					# Client side
			self.isServer = False
			self.PeerAddr = socket.gethostbyname(addr)
			self.slide_window = slide_window
			self.PeerPort = port
		# end if

		# Variables share between process and daemon
		# these variable must be accessed in the critical section
		self.CS_busy = False		# True if CS_buf contains data
		self.CS_sn_send = 0		# sequence number for send DATA 
		self.CS_sn_receive = 0	# sequence number for next DATA
		self.CS_ack_sn = 0			# sequence number for acknowledgement
		self.CS_running = True	# True after SAWsocket is active (created)
		self.CS_buf = collections.deque(maxlen=slide_window) # for message buffer
		self.CS_length = 0			# received message length

		# constant
		self.SocketIdle = float(1.0)			# 1 sec
		self.SleepIdle = float(0.1)				# 0.1 sec
		self.BufSize = BufSize
		self.lock = threading.Lock()				# for synchronization
		self.condition = threading.Condition()
		self.ReceiveD = 0						# receive daemon
	# end of __init__()
	
	def get_sn_receive(self):
		self.lock.acquire()
		sn_receive = self.CS_sn_receive
		self.lock.release()
		return sn_receive
	# end of get_sn_receive()
	
	def get_sn_send(self):
		self.lock.acquire()
		sn_send = self.CS_sn_send
		self.lock.release()
		return sn_send
	# end of get_sn_send()
	
	def add_sn_receive(self):
		self.lock.acquire()
		self.CS_sn_receive = self.CS_sn_receive + 1
		sn_receive = self.CS_sn_receive
		self.lock.release()
		return sn_receive
	# end of add_sn_receive()
	
	def add_sn_send(self):
		self.lock.acquire()
		self.CS_sn_send += 1
		sn_send = self.CS_sn_send
		self.lock.release()
		return sn_send
	# end of add_sn_send()
	
	def receive_ack(self, sn):
		self.lock.acquire()
		self.CS_ack_sn = sn
		with self.condition:
			self.condition.notify()
		self.lock.release()
	# end of receive_ack()
	
	def get_ack_sn(self):
		self.lock.acquire()
		ack_sn = self.CS_ack_sn
		self.lock.release()
		return ack_sn
	# end of get_ack_sn()
	
	def has_data(self):
		self.lock.acquire()
		busy = self.CS_busy
		self.lock.release()
		return busy
	# end of has_data()
	
	def copy2CS_buf(self, src_buf):
		self.lock.acquire()
		self.CS_buf.append(src_buf)
		self.CS_busy = (len(self.CS_buf) >= self.slide_window)
		self.lock.release()
	# end of copy2CS_buf()
	
	def copy4CS_buf(self):
		self.lock.acquire()
		ret_msg = b""
		while len(self.CS_buf) > 0:
			ret_msg += self.CS_buf.popleft()
		self.CS_busy = False
		self.lock.release() 
		return ret_msg
	# end of copy4CS_buf()
	
	def wait_data(self, timeout=3):
		with self.condition:
			is_data_available = self.condition.wait(timeout=timeout)
			return is_data_available
	# end of wait_data()
	
	def data_ready(self):
		with self.condition:
			self.condition.notify()
	# end of data_ready()
	
	def wait_ack(self):
		with self.condition:
			return self.condition.wait(self.SocketIdle)
	# end of wait_ack()
	
	def is_running(self):
		self.lock.acquire()
		running = self.CS_running
		self.lock.release()
		return running
	# end of is_running()
	
	def accept(self):
		if(not self.isServer):
			print('accept() can only be called by server!!')
			exit(1)
		# end if
		
		# Wait for SYN
		recv_msg, (rip, rport) = self.socket.recvfrom(self.BufSize)
		self.PeerAddr = rip
		self.PeerPort = rport
		if(DEBUG):
			print('Connect from IP: ' + str(self.PeerAddr) + ' port: ' + str(self.PeerPort))
			
		# Send SYN/ACK
		reply = 'SYN/ACK'
		self.socket.sendto(reply.encode('utf-8'), (self.PeerAddr, self.PeerPort))
		
		# Wait for ACK
		recv_msg, (rip, rport) = self.socket.recvfrom(self.BufSize)

		if(DEBUG):
			print('Connection from: ' + str(self.PeerAddr) + ':' + str(self.PeerPort) + ' established')
		
		# Create ReceiveD
		self.ReceiveD = ReceiveD(self.socket, self.PeerAddr, self.PeerPort, self)
	# end of accept()
	
	def connect(self):
		if(self.isServer):
			print('connect() can only be called by client!!')
			exit(1)	
		# end if
	
		# send SYN
		message = 'SYN'
		self.socket.sendto(message.encode('utf-8'), (self.PeerAddr, self.PeerPort))
		if(DEBUG):
			print('Connect to: ' + str(self.PeerAddr) + ' port: ' + str(self.PeerPort))
		
		# Receive SYN/ACK
		recv_msg, (rip, rport) = self.socket.recvfrom(self.BufSize)
		
		# send ACK
		message = 'ACK'
		self.socket.sendto(message.encode('utf-8'), (self.PeerAddr, self.PeerPort))
		if(DEBUG):
			print('Connection to: ' + str(self.PeerAddr) + ':' + str(self.PeerPort) + ' established')
		
		# Create ReceiveD
		self.ReceiveD = ReceiveD(self.socket, self.PeerAddr, self.PeerPort, self)
	# end of connect()
	
	def send(self, frames):
		success = False
		ack_sn = 0
		while(not success):
			self.CS_sn_send = ack_sn
			for buf in frames[ack_sn:]:
				length = len(buf)
				sn_send = self.get_sn_send()
				msg_type = ord('M')
				value = (msg_type, sn_send, buf.encode())
				msg_format = '!' + 'B I ' + str(length) + 's'
				s = struct.Struct(msg_format)
				packed_data = s.pack(*value)
				self.socket.sendto(packed_data, (self.PeerAddr, self.PeerPort))
				self.add_sn_send()
			
			res = self.wait_ack()
			if not res:
				ack_sn = 0
				print("Timeout!! Resend!!")
				continue
			
			ack_sn = self.get_ack_sn()
			if(ack_sn == self.get_sn_send()):
				success = True
				print('Send Success !!')
			elif(DEBUG):
				print('Send failed !! SN = ' + str(ack_sn))
		return 'ok'
		# end while
	# end of send()
	
	def receive(self):
		sn = self.get_sn_receive()
		if(not self.has_data()):
			res = self.wait_data()
			if not res:
				print("Timeout occurred while waiting for data.")
				return
		
		ret_msg = self.copy4CS_buf()
		return ret_msg
	# end of receive()
	
	def close(self):
		# Send Finish
		sn = self.get_sn_send()
		msg_format1 = '!' + 'B I ' 				# !: network order
		s = struct.Struct(msg_format1)
		value = (ord('F'), sn)
		packed_data = s.pack(*value)
		self.socket.sendto(packed_data, (self.PeerAddr, self.PeerPort))
		self.CS_running = False
		self.ReceiveD.join()						# Waiting receive daemon closed
		self.socket.close()
	# end of close()
# end of class SAWSocket

class ReceiveD(threading.Thread):
	def __init__(self, socket: socket.socket, sAddr, sPort, SAWSocket: SAWSocket):
		super().__init__(name = 'ReceiveD')
		self.socket = socket
		self.peerAddr = sAddr
		self.peerPort = sPort
		self.data = SAWSocket
		self.running = True
		self.start()
	# end of __init__()
	
	def run(self):
		resend_flag = 1
		receive_flag = 1
		print(self.data)
		block_msg = random.randint(0, self.data.slide_window - 1)
		while(self.data.is_running()):
			# Receive a message
			recv_msg, (rip, rport) = self.socket.recvfrom(self.data.BufSize)
			length = len(recv_msg) - 5
			msg_format1 = '!' + 'B I ' + str(length) + 's'				# !: network order
			msg_format2 = '!' + str(length) + 's'
			s = struct.Struct(msg_format1)
			data = s.unpack(recv_msg)
			msg_type = data[0]
			msg_sn = data[1]
			msg_value = (data[2], )
			s = struct.Struct(msg_format2)
			msg_msg = s.pack(*msg_value)
			
			if(msg_type == ord('M')):
				if receive_flag == 1 and msg_sn == block_msg:
					receive_flag = 0
					continue
				
				if(msg_sn == self.data.get_sn_receive()):		# receive a new message
					print(msg_type, msg_sn)
					resend_flag = 1

					self.data.add_sn_receive()
					while(self.data.has_data()):							# data still in CS_buf
						time.sleep(self.data.SleepIdle)
				
					self.data.copy2CS_buf(msg_msg)
					if self.data.CS_busy:
						self.data.data_ready()											    # notify												
						msg_sn = msg_sn + 1													# for acknowledgement
						msg_format1 = '!' + 'B I ' 											# !: network order
						s = struct.Struct(msg_format1)
						value = (ord('A'), msg_sn)
						packed_data = s.pack(*value)
						self.socket.sendto(packed_data, (self.peerAddr, self.peerPort))
						self.data.CS_sn_receive %= self.data.slide_window
						receive_flag = 1
						block_msg = random.randint(0, self.data.slide_window - 1)
				elif msg_sn > self.data.get_sn_receive() and resend_flag:
					print('Not Received message. SN = ' + str(self.data.get_sn_receive()))
					resend_flag = 0
					msg_format1 = '!' + 'B I ' 											# !: network order
					s = struct.Struct(msg_format1)
					value = (ord('A'), self.data.get_sn_receive())
					packed_data = s.pack(*value)
					self.socket.sendto(packed_data, (self.peerAddr, self.peerPort))
				
			elif(msg_type == ord('A')):
				self.data.receive_ack(msg_sn)
			elif(msg_type == ord('F')):
				# Reply ACK
				print(msg_type, msg_sn)
				msg_format1 = '!' + 'B I ' 				# !: network order
				s = struct.Struct(msg_format1)
				value = (ord('A'), msg_sn)
				packed_data = s.pack(*value)
				self.socket.sendto(packed_data, (self.peerAddr, self.peerPort))
				self.data.CS_running = False
			else:
				if(DEBUG):
					print('Message error. SN = ' + str(msg_sn))
		# end of while
		if(DEBUG):
			print('Receive daemon closed()')
	# end of run()
# end of class ReceiveD

if __name__ == '__main__':
	print('Hello!!')

