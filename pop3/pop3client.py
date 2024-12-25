####################################################
#  Network Programming - Unit 3 Application based on TCP         
#  Program Name: pop3client.py                                      			
#  The program is a simple POP3 client.            		
#  2021.08.03                                                   									
####################################################
import sys, re
import socket
from getpass import getpass

PORT = 110
BUFF_SIZE = 1024

cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def ParseMessage(msg):
	line = []
	newstring = ''
	for i in range(len(msg)):
		if(msg[i] == '\n'):
			line.append(newstring)
			newstring = ''
		else:
			newstring += msg[i]
	return line

def ParseHeader(msg):
	headers = []
	INFO = ["Date", "Subject", "From", "To"]
	for info in INFO:
		pattern = f"^({info}: .*)$"
		match_header = re.search(pattern, msg, re.MULTILINE)
		headers.append(match_header.group(1))
	return headers

def ParseContent(msg):
	lines = msg.split('\r\n')
	for idx, line in enumerate(lines):
		if len(line) == 0:
			return lines[idx + 1:]

def generate_cmd(cmd: str):
	return cmd + "\r\n"	

def update():
	cSocket.send(generate_cmd(f"QUIT").encode('utf-8'))
	reply = cSocket.recv(BUFF_SIZE).decode('utf-8')
	print(reply)

def run(cmd : int):
	# 秀出 mailbox 中有幾封 mail
	if cmd == 1:
		cSocket.send(generate_cmd("LIST").encode('utf-8'))
		reply = cSocket.recv(BUFF_SIZE).decode('utf-8')
		line = ParseMessage(reply)
		num = len(line) - 2
		print('Mailbox has %d mails\n' % num)

	# 刪除第 nn 封信
	if cmd == 2:
		email_id = int(input("Enter your email id："))
		cSocket.send(generate_cmd(f"DELE {email_id}").encode('utf-8'))
		reply = cSocket.recv(BUFF_SIZE).decode('utf-8')
		print(reply)

	# 列出信箱中每一封 mail 的寄信時間、信件主題、寄件人、收件人
	if cmd == 3:
		email_id = int(input("Enter your email id："))

		print()
		cSocket.send(generate_cmd(f"TOP {email_id} 10").encode('utf-8'))
		reply = cSocket.recv(BUFF_SIZE).decode('utf-8')
		headers = ParseHeader(reply)
		for header in headers:
			print(header)

	# 列出第 nn 封信的內容 (如信件已編碼需解碼)
	if cmd == 4:
		email_id = int(input("Enter your email id："))

		print()
		cSocket.send(generate_cmd(f"TOP {email_id} 10").encode('utf-8'))
		reply = cSocket.recv(BUFF_SIZE).decode('utf-8')
		contents = ParseContent(reply)
		for ctx in contents:
			print(ctx)

def main():
	if(len(sys.argv) < 2):
		print("Usage: python3 pop3client.py ServerIP")
		exit(1)

	serverIP = socket.gethostbyname(sys.argv[1])
	
	name = input('Username: ')
	password = getpass('Password: ') 

	print('Connecting to %s port %s' % (serverIP, PORT))
	cSocket.connect((serverIP, PORT))

	try:
		reply = cSocket.recv(BUFF_SIZE).decode('utf-8')
		print('Receive message: %s' % reply)
		if(reply[0] != '+'):
			return

		cmd = generate_cmd('USER ' + name)
		cSocket.send(cmd.encode('utf-8'))
		reply = cSocket.recv(BUFF_SIZE).decode('utf-8')
		print('Receive message: %s' % reply)
		if(reply[0] != '+'):
			return
	
		cmd = generate_cmd('PASS ' + password)
		cSocket.send(cmd.encode('utf-8'))
		reply = cSocket.recv(BUFF_SIZE).decode('utf-8')
		print('Receive message: %s' % reply)
		if(reply[0] != '+'):
			return

		while True:
			cmd = input("Command：")
			if cmd == 5:
				update()
				break
			run(int(cmd))

	except socket.error as e:
		print('Socket error: %s' % str(e))
	except Exception as e:
		print('Other exception: %s' % str(e))

	print('Closing connection.')
	cSocket.close()

if __name__ == '__main__':
	main()
