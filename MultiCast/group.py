import socket, struct

def JoinGroup(s:socket.socket, group_addr, flag):	# flag = True (join) / False (leave)
	group = socket.inet_aton(group_addr)
	mreq = struct.pack('4sL', group, socket.INADDR_ANY)
	if flag:
		cmd = socket.IP_ADD_MEMBERSHIP
	else:
		cmd = socket.IP_DROP_MEMBERSHIP
		
	s.setsockopt(socket.IPPROTO_IP, cmd, mreq)