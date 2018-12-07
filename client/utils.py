import pickle
import socket
import struct

ip = 'localhost'
port = 9999

fps = 20

class Global:
    sock_server = None
    sock_game = None
    game_thread = None
    login = ''

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


def fields_are_ok(fields):
    is_ok = True
    for field in fields:
        if field.text().isspace() or not field.text() or ' ' in field.text():
            is_ok = False
            
    return is_ok


def connect_to_server():
    Global.sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ip, port)
    Global.sock_server.connect(server_address)

def connect_to_server_game():
    Global.sock_game = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ip, port)
    Global.sock_game.connect(server_address)
