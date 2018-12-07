import socket
import utils
import clientthread
import database
import sys
import game

# Create tcp for server
sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('0.0.0.0', 9999)
sock_server.bind(server_address)
sock_server.listen(50)

utils.print_log('', "Serveur lancé")

try:
    database.Database.connect()
except Exception as e:
    utils.print_log('', str(e))
    sys.exit()

while True:
    # Wait for client connection
    sock_client, client_address = sock_server.accept()

    utils.print_log('', "Client accepté")

    client_thread = clientthread.ClientThread(sock_client)
    client_thread.start()
