import utils
import commands
import sys
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import *
from game import Game
from ingame import InGameWindow

class CreateGameWindow(QtGui.QMainWindow, uic.loadUiType("ui/editgame.ui")[0]):
    def __init__(self, parent = None, game = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.parent = parent
        self.game = game

        # Disable creation button
        self.btnCreateGame.setEnabled(False)
        self.sbxNbMaxPlayers.setRange(1, 12)

        # Fill the game types combobox
        types = ['FFA']
        self.cbxGameType.addItems(types)

        # Get maps and fill the map combobox
        utils.send_data(utils.Global.sock_server, commands.CMD_GET_MAPS)
        nb_of_maps = utils.recv_data(utils.Global.sock_server)
        maps = []
        for i in range(nb_of_maps):
            maps.append(str(i + 1))
        self.cbxGameMap.addItems(maps)

        # Bind events
        self.edtGameName.textChanged.connect(self.text_changed)
        self.btnCancel.clicked.connect(self.btnCancel_clicked)
        if game == None:
            self.btnCreateGame.clicked.connect(self.btnCreateGame_clicked)
        else:
            self.btnCreateGame.clicked.connect(self.btnEditGame_clicked)
            self.btnCreateGame.setText("Modifier")
            self.edtGameName.setText(self.game.name)
            self.sbxNbMaxPlayers.setValue(int(self.game.nb_max_players))
            type_index = self.cbxGameType.findText(self.game.type, QtCore.Qt.MatchFixedString)
            self.cbxGameType.setCurrentIndex(type_index)
            map_index = self.cbxGameMap.findText(str(self.game.map), QtCore.Qt.MatchFixedString)
            self.cbxGameMap.setCurrentIndex(map_index)
            self.edtGamePassword.setText(self.game.password)

    def btnEditGame_clicked(self):
        utils.send_data(utils.Global.sock_server, commands.CMD_EDIT_GAME)

        self.game.name = self.edtGameName.text()
        self.game.nb_max_players = self.sbxNbMaxPlayers.text()
        self.game.type = self.cbxGameType.currentText()
        self.game.map = self.cbxGameMap.currentText()
        self.game.password = self.edtGamePassword.text()

        utils.send_data(utils.Global.sock_server, self.game)

        self.parent.refresh()
        self.close()

    def btnCreateGame_clicked(self):
        utils.send_data(utils.Global.sock_server, commands.CMD_CREATE_GAME)

        game = Game(utils.Global.login,
            self.edtGameName.text(),
            int(self.sbxNbMaxPlayers.text()),
            self.cbxGameType.currentText(),
            int(self.cbxGameMap.currentText()),
            self.edtGamePassword.text())

        utils.send_data(utils.Global.sock_server, game)

        self.parent.refresh()

        in_game_window = InGameWindow(self.parent, True)
        in_game_window.setWindowModality(QtCore.Qt.ApplicationModal)
        in_game_window.show()

        self.close()

    def btnCancel_clicked(self):
        self.close()

    def text_changed(self):
        if self.edtGameName.text().isspace() or not self.edtGameName.text():
            self.btnCreateGame.setEnabled(False)
        else:
            self.btnCreateGame.setEnabled(True)