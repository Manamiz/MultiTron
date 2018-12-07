from PyQt4 import QtGui, uic
from PyQt4.QtGui import QLineEdit, QMessageBox
import commands
import utils


class InscriptionWindow(QtGui.QMainWindow, uic.loadUiType("ui/inscription.ui")[0]):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        # Hide password text
        self.edtPassword.setEchoMode(QLineEdit.Password)
        self.edtConfirmPassword.setEchoMode(QLineEdit.Password)
        
        self.btnInscription.setEnabled(False)

        # Bind buttons
        self.btnCancel.clicked.connect(self.btnCancel_clicked)
        self.btnInscription.clicked.connect(self.btnInscription_clicked)
        
        # Bind text edit
        self.edtUsername.textChanged.connect(self.text_changed)
        self.edtPassword.textChanged.connect(self.text_changed)
        self.edtConfirmPassword.textChanged.connect(self.text_changed)

    def btnCancel_clicked(self):
        self.close()

    def btnInscription_clicked(self):
        username = self.edtUsername.text()
        password = self.edtPassword.text()
        confirmPassword = self.edtConfirmPassword.text()
        
        if password != confirmPassword:
            QMessageBox.about(self, 'Erreur', 'Les mots de passe sont différents !')
        else:
            utils.send_data(utils.Global.sock_server, commands.CMD_INSCRIPTION)
            utils.send_data(utils.Global.sock_server, [username, password])
            response = utils.recv_data(utils.Global.sock_server)
            
            if response == commands.CMD_OK:
                QMessageBox.about(self, 'Inscription', 'Vous êtes maintenant inscrit !')
                self.close()
            else:
                QMessageBox.about(self, 'Erreur', 'Un erreur est survenue !')

    def text_changed(self):
        if utils.fields_are_ok([self.edtUsername, self.edtPassword, self.edtConfirmPassword]):
            self.btnInscription.setEnabled(True)
        else:
            self.btnInscription.setEnabled(False)
