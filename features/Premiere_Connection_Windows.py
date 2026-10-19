import tool
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QDialog, QVBoxLayout, QFrame,QHBoxLayout,QFormLayout,QLineEdit

class Premiere_Connection_Windows(QDialog):
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

        #Bouton de validation
        btn_valider = QPushButton("Valider le mot de passe")
        layout_principal.addWidget(btn_valider)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("features/style.qss", "r") as fichier:
        app.setStyleSheet(fichier.read())

    fenetre = Premiere_Connection_Windows()
    fenetre.show()
    sys.exit(app.exec())