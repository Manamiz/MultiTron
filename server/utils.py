import pickle
import struct
import time

class Global:
    players = []
    games = []

def send_data(sock, data):
	packet = pickle.dumps(data)
	length = struct.pack('!I', len(packet))
	
	packet = length + packet
	
	sock.sendall(packet)

def recv_data(sock):
	data_length = recvall(sock, 4)
	
	if not data_length:
		return None

	data_length = struct.unpack('!I', data_length)[0]
	
	return pickle.loads(recvall(sock, data_length))
	

def recvall(sock, n):
	data = b''
	while len(data) < n:
		packet = sock.recv(n - len(data))
		
		if not packet:
			return None
			
		data += packet
	
	return data

def print_log(user, message):
    if user == '':
        print(time.strftime("%d.%m.%Y") + ' ' + time.strftime("%H:%M:%S") + \
        ' : ' + message)
    else:
        print(user + ' --- ' + time.strftime("%d.%m.%Y") + ' ' + time.strftime("%H:%M:%S") + \
        ' : ' + message)
