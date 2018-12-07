from threading import Thread, Lock
import database
import utils
import os
from commands import *
from player import Player
from gamethread import GameThread

mutex = Lock()

class ClientThread(Thread):
    def __init__(self, sock_client):
        Thread.__init__(self)
        self.sock_client = sock_client

    def run(self):
        current_player_login = ''

        while True:
            # Get command list
            try:
                command = utils.recv_data(self.sock_client)
            except Exception as e:
                utils.print_log(current_player_login, str(e))
                self.deconnect_client(current_player_login)
                break

            if command == None:
                self.deconnect_client(current_player_login)
                mutex.acquire()
                for game in utils.Global.games:
                    if game.creator == current_player_login:
                        utils.Global.games.remove(game)
                mutex.release()
                break

            # Launch action based on command
            if command == CMD_INSCRIPTION:
                inscription_infos = utils.recv_data(self.sock_client)
                username = inscription_infos[0]
                password = inscription_infos[1]
                utils.print_log(current_player_login, "Inscription en cours : " + username + " " + password)
                result = database.Database.insert_client(username, password)
                
                if result:
                    utils.print_log(current_player_login, "Inscription réussie")
                    utils.send_data(self.sock_client, CMD_OK)
                else:
                    utils.print_log(current_player_login, "Inscription échouée (nom d'utilisateur déjà utilisé)")
                    utils.send_data(self.sock_client, CMD_NOT_OK)
            elif command == CMD_CONNECTION:
                connection_infos = utils.recv_data(self.sock_client)
                username = connection_infos[0]
                password = connection_infos[1]
                utils.print_log(current_player_login, "Connexion en cours : " + username + " " + password)
                result = database.Database.check_client(username, password)
                ok = True
                
                if result:
                    # On check s'il y est déjà connecté
                    for player in utils.Global.players:
                        if username == player.login:
                            utils.print_log(current_player_login, "Connexion échouée (déjà connecté)")
                            utils.send_data(self.sock_client, CMD_NOT_OK)
                            ok = False
                    if ok:
                        utils.print_log(current_player_login, "Connexion réussie")
                        current_player_login = username
                        mutex.acquire()
                        utils.Global.players.append(Player(username))
                        mutex.release()
                        utils.send_data(self.sock_client, CMD_OK)
                else:
                    utils.print_log(current_player_login, "Connexion échouée (nom d'utilisateur ou mot de passe incorrect)")
                    utils.send_data(self.sock_client, CMD_NOT_OK)
            elif command == CMD_GET_SCORES:
                utils.print_log(current_player_login, 'Demande des scores en cours')
                scores = database.Database.get_all_scores()
                utils.send_data(self.sock_client, scores)
            elif command == CMD_GET_MAPS:
                utils.print_log(current_player_login, "Demande des maps en cours (création d'une partie)")
                DIR = 'map/'
                nb_of_maps = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
                utils.send_data(self.sock_client, nb_of_maps)
            elif command == CMD_GET_GAMES:
                utils.print_log(current_player_login, 'Demande des parties en cours (affichage des parties)')
                utils.send_data(self.sock_client, utils.Global.games)
            elif command == CMD_CREATE_GAME:
                utils.print_log(current_player_login, "Création d'une partie")
                game = utils.recv_data(self.sock_client)
                mutex.acquire()
                utils.Global.games.append(game)
                mutex.release()
            elif command == CMD_JOIN_GAME:
                utils.print_log(current_player_login, "Rejoins une partie")
                infos = utils.recv_data(self.sock_client)
                game_id = int(infos[0])
                player = infos[1]
                mutex.acquire()
                utils.Global.games[game_id].players.append(player)
                mutex.release()
            elif command == CMD_GET_GAME:
                utils.print_log(current_player_login, "Demande les informations d'une partie")
                login = utils.recv_data(self.sock_client)
                not_send = True
                for game in utils.Global.games:
                    if login in game.players:
                        utils.send_data(self.sock_client, game)
                        not_send = False
                        break

                if not_send:
                    utils.send_data(self.sock_client, None)
            elif command == CMD_LEAVE_GAME:
                utils.print_log(current_player_login, "Quitte une partie")
                for game in utils.Global.games:
                    if login in game.players:
                        if login == game.creator:
                            mutex.acquire()
                            utils.Global.games.remove(game)
                            mutex.release()
                            break
                        else:
                            mutex.acquire()
                            game.players.remove(login)
                            mutex.release()
                            break
            elif command == CMD_EDIT_GAME:
                utils.print_log(current_player_login, "Edition d'une partie")
                current_game = utils.recv_data(self.sock_client)
                for game in utils.Global.games:
                    if game.creator == current_game.creator:
                        game.name = current_game.name
                        game.nb_max_players = current_game.nb_max_players
                        game.type = current_game.type
                        game.map = current_game.map
                        game.password = current_game.password
            elif command == CMD_STOCK_SOCK_GAME:
                utils.print_log(current_player_login, "Stockage du socket pour le jeu")
                login = utils.recv_data(self.sock_client)
                for player in utils.Global.players:
                    if player.login == login:
                        player.sock = self.sock_client
                break
            elif command == CMD_LAUNCH_GAME:
                utils.print_log(current_player_login, "Lancement d'une partie")
                creator_login = utils.recv_data(self.sock_client)

                players = []
                current_game = None
                id = 1

                for game in utils.Global.games:
                    if creator_login == game.creator:
                        for player in utils.Global.players:
                            for game_player in game.players:
                                if player.login == game_player:
                                    players.append(player)
                                    current_game = game
                                    utils.send_data(player.sock, CMD_LAUNCH_GAME)

                                    utils.send_data(player.sock, id)

                                    id = id + 1

                                    file = open('map/map' + str(game.map) + '.txt', 'r')
                                    nb_tiles_x = int(file.readline())
                                    nb_tiles_y = int(file.readline())
                                    map = []
                                    for i in range(nb_tiles_y):
                                        line = file.readline().rstrip()
                                        map.append([])
                                        for j in line.split(' '):
                                            map[i].append(int(j))

                                    file.close()

                                    utils.send_data(player.sock, map)

                gameThread = GameThread(game, players)
                gameThread.start()

    def deconnect_client(self, login):
        utils.print_log(login, "Client deconnecté")
        for player in utils.Global.players:
            if login == player.login:
                mutex.acquire()
                utils.Global.players.remove(player)
                mutex.release()
                break
