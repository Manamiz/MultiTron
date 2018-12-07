import pickle
import utils
import random
import time
from commands import *
from player import Player
from threading import Thread, Lock
import database

class GameThread(Thread):
    def __init__(self, game, players):
        Thread.__init__(self)
        self.game = game
        self.players = players

    def run(self):

        colors = []
        logins = []
        id = 1
        for player in self.players:
            colors.append((id * random.randint(0, 255) % 255, id * random.randint(0, 255) % 255, id * random.randint(0, 255) % 255))
            logins.append(player.login)
            id = id + 1

        for player in self.players:
            utils.send_data(player.sock, colors)
            utils.send_data(player.sock, logins)

        running = True
        while running:

            players_grid = []

            idKill = []
            idLost = []
            for player in self.players:
                idKill.append(utils.recv_data(player.sock))

                idLost.append(utils.recv_data(player.sock))

                player_grid = utils.recv_data(player.sock)

                players_grid.append(player_grid)

            send_grid = players_grid[0]
            for grid in players_grid:
                for i in range(96):
                    for j in range(96):
                        if grid[i][j] != 0 and send_grid[i][j] == 0:
                            send_grid[i][j] = grid[i][j]

            win = []
            scores = []
            for player in self.players:
                utils.send_data(player.sock, idKill)
                utils.send_data(player.sock, idLost)
                utils.send_data(player.sock, send_grid)
                scores.append(utils.recv_data(player.sock))
                win.append(utils.recv_data(player.sock))

            tmp = False
            for w in win:
                if w:
                    tmp = True
                else:
                    tmp = False

            if tmp:
                for player in self.players:
                    utils.send_data(player.sock, True)

                running = False
            else:
                for player in self.players:
                    utils.send_data(player.sock, False)


        for i in range(len(self.players)):
            database.Database.update_scores(self.players[i].login, scores[i])