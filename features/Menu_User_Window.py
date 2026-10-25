import tool
import sys
import pwd as p
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QDialog, QVBoxLayout,QHBoxLayout,QWidget
from PyQt6.QtWidgets import  QLineEdit


class Menu_User_Window(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setGeometry(250, 100, 1000, 750)
        self.setWindowTitle("IPPY")
        self.menuW = None
        # 1. Layout principal de la fenêtre
        layout_principal = QVBoxLayout(self)

        layout_haut=QHBoxLayout()
        layout_haut.setContentsMargins(150, 100, 150, 200)

        formulaireUser = QVBoxLayout()
        # Bouton changer de mot de passe
        btn_changer_mdp = QPushButton("Changer de mot de passe")
        formulaireUser.addWidget(btn_changer_mdp)
        #Bouton changer de nom d'utilisateur
        btn_changer_username = QPushButton("Changer de nom d'utilisateur")
        formulaireUser.addWidget(btn_changer_username)
        #bouton de retour
        btn_retour = QPushButton("Retour")
        btn_retour.clicked.connect(self.close)
        formulaireUser.addWidget(btn_retour)

        layout_haut.addLayout(formulaireUser)     
        layout_principal.addLayout(layout_haut)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("features/style.qss", "r") as fichier:
        app.setStyleSheet(fichier.read())

    fenetre = Menu_User_Window()
    fenetre.show()
    sys.exit(app.exec())