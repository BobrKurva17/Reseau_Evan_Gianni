import tool 
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QDialog, QVBoxLayout,QHBoxLayout,QWidget
from PyQt6.QtWidgets import  QLineEdit
import menuWindow

class ValidationInput_Window(QDialog):
    def __init__(self, parent=None):
            super().__init__(parent)

            self.setGeometry(250, 100, 1000, 750)
            self.setWindowTitle("IPPY")
            self.menuW = None
            # 1. Layout principal de la fenêtre
            layout_principal = QVBoxLayout(self)

            layout_haut=QHBoxLayout()
            layout_haut.setContentsMargins(150, 100, 150, 200)
            # 2. Widget conteneur pour la saisie de l'IP
            Widget_input = QWidget()
            Widget_input.setObjectName("conteneur_action")

            # 3. Layout du widget de saisie
            layout_conteneur_input = QVBoxLayout(Widget_input)
            

            # 4. Éléments de saisie
            self.message_erreur = QLabel("")
            self.message_erreur.setObjectName("message_erreur")

            self.champ_ip = QLineEdit()
            self.champ_ip.setObjectName("label_chemin")

            label_input = QLabel("Entrer votre adresse IP au format 192.168.12.0")
            label_input.setObjectName("label_action")

            layout_conteneur_input.addWidget(label_input, alignment=Qt.AlignmentFlag.AlignCenter)
            layout_conteneur_input.addWidget(self.champ_ip, alignment=Qt.AlignmentFlag.AlignCenter)
            layout_conteneur_input.addWidget(self.message_erreur, alignment=Qt.AlignmentFlag.AlignCenter)

            # 5. Layout des boutons
            layout_bas = QHBoxLayout()

            bouton_retour = QPushButton("Retour")
            bouton_valider = QPushButton("Valider l'IP")

            layout_bas.addWidget(bouton_retour,alignment=Qt.AlignmentFlag.AlignLeft)
            layout_bas.addWidget(bouton_valider,alignment=Qt.AlignmentFlag.AlignRight)

            # 6. Composition finale de la fenêtre
            layout_haut.addWidget(Widget_input)
            layout_principal.addLayout(layout_haut)
            layout_principal.addLayout(layout_bas)

            #action 
            bouton_valider.clicked.connect(lambda: tool.validIP(self))
            bouton_retour.clicked.connect(self.appel_menuWindow)

    def appel_menuWindow(self):
    #instanciation des autres fenêtres possibles 
            if self.menuW is None :
                self.menuW=menuWindow.Menu_Window()
                self.menuW.show() 
                self.close()
            else: 
                self.menuW.close()
                self.menuW = None
            


if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("features/style.qss", "r") as fichier:
        app.setStyleSheet(fichier.read())

    fenetre = ValidationInput_Window()
    fenetre.show()
    sys.exit(app.exec())
