import sys
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import *
import commands
import utils
from inscription import InscriptionWindow
from displaygames import DisplayGamesWindow
from gamethread import GameThread

class ConnectionWindow(QtGui.QMainWindow, uic.loadUiType("ui/connection.ui")[0]):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        # Hide password text
        self.edtPassword.setEchoMode(QLineEdit.Password)
        
        self.btnConnection.setEnabled(False)

        # Bind buttons
        self.btnLeave.clicked.connect(self.btnLeave_clicked)
        self.btnInscription.clicked.connect(self.btnInscription_clicked)
        self.btnConnection.clicked.connect(self.btnConnection_clicked)
        
        # Bind text edit
        self.edtUsername.textChanged.connect(self.text_changed)
        self.edtPassword.textChanged.connect(self.text_changed)

    def btnLeave_clicked(self):
        sys.exit()

    def btnInscription_clicked(self):
        inscription_window = InscriptionWindow(self)
        inscription_window.setWindowModality(QtCore.Qt.ApplicationModal)
        inscription_window.show()

    def btnConnection_clicked(self):
        username = self.edtUsername.text()
        password = self.edtPassword.text()
        
        utils.send_data(utils.Global.sock_server, commands.CMD_CONNECTION)
        utils.send_data(utils.Global.sock_server, [username, password])
        
        response = utils.recv_data(utils.Global.sock_server)
        
        if response == commands.CMD_OK:
            utils.Global.login = username

            # Launch game socket
            utils.connect_to_server_game()
            utils.send_data(utils.Global.sock_game, commands.CMD_STOCK_SOCK_GAME)
            utils.send_data(utils.Global.sock_game, username)
            utils.Global.game_thread = GameThread()
            utils.Global.game_thread.start()

            display_games_window = DisplayGamesWindow(self)
            display_games_window.show()
            self.hide()
        else:
            QMessageBox.about(self, 'Erreur', 'Une erreur est survenue')

    def text_changed(self):
        if utils.fields_are_ok([self.edtUsername, self.edtPassword]):
            self.btnConnection.setEnabled(True)
        else:
            self.btnConnection.setEnabled(False)
