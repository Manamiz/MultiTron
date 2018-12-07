import sys
import socket
import utils
from PyQt4 import QtGui
from connection import ConnectionWindow

try:
    utils.connect_to_server()
except Exception as e:
    QMessageBox.about(self, 'Erreur', 'Impossible de se connecter au serveur !')

app = QtGui.QApplication(sys.argv)
connWindow = ConnectionWindow(None)
connWindow.show()
app.exec_()
