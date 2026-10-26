
import sys
from . import pwd
from .tool import obtenir_connexion
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QDialog, QVBoxLayout, QFrame,QHBoxLayout,QFormLayout,QLineEdit,QMessageBox

class Premiere_Connection_Windows(QDialog):
    def valider_mot_de_passe(self):
        self.label_erreur.setText("")  # Réinitialiser le message d'erreur
        mdp = self.input_mdp.text()
        mdpConfirm = self.input_confirmation.text()
        utilisateur = self.input_username.text()

        if(not utilisateur):
            self.label_erreur.setText("Le nom d'utilisateur ne peut pas être vide")
            return False

        if(mdp != mdpConfirm):
            self.label_erreur.setText("Les mots de passe ne correspondent pas")
            return False

        if(not pwd.verifierMotDePasse(mdp, self)):
            return False

        self.enregistrement_super_admin()

    def enregistrement_super_admin(self):
        cnx = obtenir_connexion(self)
        cursor = cnx.cursor()
        codeSecret = pwd.genererCodeSecret()
        QMessageBox.warning(self, "Code secret généré", f"Le code secret généré est : {codeSecret}\nVeuillez le noter quelque part, il sera nécessaire pour la récupération du mot de passe.")
        superAdmin = {
            "username": self.input_username.text(),
            "pswd": pwd.hash_password(self.input_mdp.text()),
            "roles": "superadmin",
            "codeSecret": pwd.hash_password(codeSecret)
        }
        cursor.execute("INSERT INTO user (username, pswd, roles, codeSecret) VALUES (%s, %s, %s, %s)", 
                                (superAdmin["username"], superAdmin["pswd"], superAdmin["roles"], superAdmin["codeSecret"]))  
        cnx.commit()
        self.close()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setGeometry(250, 100, 1000, 750)
        self.setWindowTitle("IPPY")
        self.menuW = None
        # 1. Layout principal de la fenêtre
        layout_principal = QVBoxLayout(self)

        layout_haut=QHBoxLayout()
        layout_haut.setContentsMargins(150, 100, 150, 200)

        formulaireConnexion = QFormLayout()
        # Champ nom d'utilisateur
        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText("Nom d'utilisateur")
        formulaireConnexion.addRow("Nom d'utilisateur:", self.input_username)
        # Champ mot de passe principal
        self.input_mdp = QLineEdit()
        self.input_mdp.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_mdp.setPlaceholderText("Minimum 8 caractères dont 1 chiffre, 1 majuscule et 1 caractère spécial (!@#$%&*?)")
        formulaireConnexion.addRow("Mot de passe:", self.input_mdp)
        
        # Champ de confirmation
        self.input_confirmation = QLineEdit()
        self.input_confirmation.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_confirmation.setPlaceholderText("Retapez votre mot de passe")
        formulaireConnexion.addRow("Confirmation du mot de passe:", self.input_confirmation)

        layout_haut.addLayout(formulaireConnexion)
        layout_principal.addLayout(layout_haut)

        # Label pour les messages d'erreur
        self.label_erreur = QLabel()
        self.label_erreur.setStyleSheet("color: red;")

        layout_principal.addWidget(self.label_erreur)

        #Bouton de validation
        btn_valider = QPushButton("Valider le mot de passe")
        btn_valider.clicked.connect(self.valider_mot_de_passe)
        layout_principal.addWidget(btn_valider)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("features/style.qss", "r") as fichier:
        app.setStyleSheet(fichier.read())

    fenetre = Premiere_Connection_Windows()
    fenetre.show()
    sys.exit(app.exec())