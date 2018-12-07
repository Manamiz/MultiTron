import utils
import commands
import sys
import time
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import *
from game import Game
import creategame

class InGameWindow(QtGui.QMainWindow, uic.loadUiType("ui/ingame.ui")[0]):
    def __init__(self, parent = None, is_creator = False):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.parent = parent
        self.game = None

        # Bind buttons
        self.btnLeave.clicked.connect(self.btnLeave_clicked)
        self.btnRefresh.clicked.connect(self.btnRefresh_clicked)
        self.btnLaunch.clicked.connect(self.btnLaunch_clicked)
        self.btnEdit.clicked.connect(self.btnEdit_clicked)

        # Hide buttons for non creator
        if not is_creator:
            self.btnLaunch.hide()
            self.btnEdit.hide()

        self.parent.refresh()
        self.refresh()

    def closeEvent(self, event):
        self.leave_game()

    def btnLeave_clicked(self):
        self.leave_game()
        self.close()

    def btnLaunch_clicked(self):
        utils.send_data(utils.Global.sock_server, commands.CMD_LAUNCH_GAME)
        utils.send_data(utils.Global.sock_server, utils.Global.login)

    def btnRefresh_clicked(self):
        self.refresh()

    def btnEdit_clicked(self):
        create_game_window = creategame.CreateGameWindow(self, self.game)
        create_game_window.setWindowModality(QtCore.Qt.ApplicationModal)
        create_game_window.show()

    def refresh(self):
        # Get current game
        utils.send_data(utils.Global.sock_server, commands.CMD_GET_GAME)
        utils.send_data(utils.Global.sock_server, utils.Global.login)
        game = utils.recv_data(utils.Global.sock_server)

        if game == None:
            QMessageBox.about(self, 'Erreur', "La partie n'existe plus ! Le créateur a dû déserter !")
            self.parent.refresh()
            self.close()
            return

        self.game = game
        self.lblGameName.setText(game.name)

        self.tblPlayers.clear()
        for player in game.players:
            self.tblPlayers.addItem(player)

    def leave_game(self):
        utils.send_data(utils.Global.sock_server, commands.CMD_LEAVE_GAME)
        utils.send_data(utils.Global.sock_server, utils.Global.login)

        self.parent.refresh()