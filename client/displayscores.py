import utils
import commands
import sys
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QTableWidgetItem, QMessageBox, QHeaderView

class ScoresWindow(QtGui.QMainWindow, uic.loadUiType("ui/scores.ui")[0]):
    def __init__(self, parent = None, admin = False):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        header_labels = ('Pseudo', 'Score')
        self.tblScores.setColumnCount(2)
        self.tblScores.setHorizontalHeaderLabels(header_labels)
        self.tblScores.horizontalHeader().setResizeMode(QHeaderView.Stretch)

        # Bind buttons
        self.btnLeave.clicked.connect(self.btnLeave_clicked)
        if not admin:
            self.btnEdit.hide()
            self.btnDelete.hide()

        # Get score list
        utils.send_data(utils.Global.sock_server, commands.CMD_GET_SCORES)
        scores = utils.recv_data(utils.Global.sock_server)
        
        self.tblScores.setRowCount(len(scores))
        row = 0
        for (login, score) in scores:
            self.tblScores.setItem(row, 0, QTableWidgetItem(login))
            self.tblScores.setItem(row, 1, QTableWidgetItem(str(score)))
            row = row + 1

    def btnLeave_clicked(self):
        self.close()