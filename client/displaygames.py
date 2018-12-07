import utils
import commands
import sys
import socket
import os
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import *
from displayscores import ScoresWindow
from creategame import CreateGameWindow
from ingame import InGameWindow

class DisplayGamesWindow(QtGui.QMainWindow, uic.loadUiType("ui/displaygames.ui")[0]):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        # Bind buttons
        self.btnLeave.clicked.connect(self.btnLeave_clicked)
        self.btnRefresh.clicked.connect(self.btnRefresh_clicked)
        self.btnCreateGame.clicked.connect(self.btnCreateGame_clicked)
        self.btnDisplayScores.clicked.connect(self.btnDisplayScores_clicked)
        self.btnJoinGame.clicked.connect(self.btnJoinGame_clicked)

        self.lblAvailablesGames.setText("Parties disponibles - " + utils.Global.login)
        self.tblGames.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.passwords = []

        self.refresh()

    def closeEvent(self, event):
        utils.Global.sock_game.close()
        os._exit(0)

    def btnLeave_clicked(self):
        utils.Global.sock_game.close()
        os._exit(0)

    def btnCreateGame_clicked(self):
        create_game_window = CreateGameWindow(self)
        create_game_window.setWindowModality(QtCore.Qt.ApplicationModal)
        create_game_window.show()

    def btnDisplayScores_clicked(self):
        scores_window = ScoresWindow(self)
        scores_window.setWindowModality(QtCore.Qt.ApplicationModal)
        scores_window.show()

    def btnRefresh_clicked(self):
        self.refresh()

    def btnJoinGame_clicked(self):
        row = 0
        # Game selected ?
        try:
            row = self.tblGames.currentItem().row()
        except Exception as e:
            QMessageBox.about(self, 'Erreur', 'Veuillez sélectionner une partie !')
            return

        # Game full ?
        nb_current_players = int(self.tblGames.item(row, 1).text().split('/')[0])
        nb_max_players = int(self.tblGames.item(row, 1).text().split('/')[1])
        if nb_current_players == nb_max_players:
            QMessageBox.about(self, 'Erreur', 'La partie est pleine !')
            return

        # Password on game ?
        if self.tblGames.item(row, 5).text() == 'Oui':
            text, ok = QtGui.QInputDialog.getText(self, 'Mot de passe',
            'Entrez le mot de passe de la partie :')

            if ok:
                if str(text) != self.passwords[row]:
                    QMessageBox.about(self, 'Erreur', 'Mot de passe incorrect')
                    return

        # Send data to add player in game
        utils.send_data(utils.Global.sock_server, commands.CMD_JOIN_GAME)
        utils.send_data(utils.Global.sock_server, [row, utils.Global.login])

        in_game_window = InGameWindow(self, False)
        in_game_window.setWindowModality(QtCore.Qt.ApplicationModal)
        in_game_window.show()

    def refresh(self):
        # Get games list
        utils.send_data(utils.Global.sock_server, commands.CMD_GET_GAMES)
        games = utils.recv_data(utils.Global.sock_server)

        self.tblGames.clear()
        
        header_labels = ('Nom', 'Nombre de joueurs', 'Type', 'Carte', 'En cours ?', 'Mot de passe ?')
        self.tblGames.setColumnCount(6)
        self.tblGames.setHorizontalHeaderLabels(header_labels)
        self.tblGames.horizontalHeader().setResizeMode(QHeaderView.Stretch)

        self.tblGames.setRowCount(len(games))
        self.passwords.clear()
        row = 0
        for game in games:
            self.tblGames.setItem(row, 0, QTableWidgetItem(game.name))
            self.tblGames.setItem(row, 1, QTableWidgetItem(str(len(game.players)) + "/" + str(game.nb_max_players)))
            self.tblGames.setItem(row, 2, QTableWidgetItem(game.type))
            self.tblGames.setItem(row, 3, QTableWidgetItem(str(game.map)))
            self.tblGames.setItem(row, 4, QTableWidgetItem('Oui' if game.is_running else 'Non'))
            self.tblGames.setItem(row, 5, QTableWidgetItem('Non' if game.password == '' else 'Oui'))
            self.passwords.append(game.password)
            row = row + 1
