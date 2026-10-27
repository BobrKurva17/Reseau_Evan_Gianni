from . import tool 
import sys
# --- import outils pyside --- # 
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QDialog, QVBoxLayout,QHBoxLayout,QWidget
from PyQt6.QtWidgets import  QLineEdit
# --- import fenêtre --- # 
from . import menuWindow

class ValidationInput_Window(QDialog):
    def __init__(self, parent=None):
            super().__init__(parent)

            self.setGeometry(250, 100, 1000, 750)
            self.setWindowTitle("IPPY")
            # --- instances des fenêtres appelées = null --- #
            self.menuW = None
            # --- Layout principal de la fenêtre --- #
            layout_principal = QVBoxLayout(self)
            # --- layout haut (titre) --- #
            layout_haut=QVBoxLayout()
            layout_haut.setContentsMargins(150, 100, 150, 200)

            label_titre=QLabel("Validation adresse IP")
            label_titre.setObjectName("label_titre")
            label_titre.setFixedSize(300,50)
            label_titre.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # --- widget contenant le bloc d'action utilisateur --- #
            Widget_input = QWidget()
            Widget_input.setObjectName("conteneur_action")

            # --- Layout du widget action utilisateur --- #
            layout_conteneur_input = QVBoxLayout(Widget_input)
            

            # --- labels de validation --- #
            self.message_erreur = QLabel("")
            self.message_erreur.setObjectName("message_erreur")

            self.message_valide = QLabel("")
            self.message_valide.setObjectName("message_valide")
            # --- champ et label associé aux actions utilisateur --- #
            self.champ_ip = QLineEdit()
            self.champ_ip.setObjectName("label_chemin")

            label_input = QLabel("Entrer votre adresse IP au format 192.168.12.0")
            label_input.setObjectName("label_action")
            # --- composition du layout d'actions --- #
            layout_conteneur_input.addWidget(label_input, alignment=Qt.AlignmentFlag.AlignCenter)
            layout_conteneur_input.addWidget(self.champ_ip, alignment=Qt.AlignmentFlag.AlignCenter)
            layout_conteneur_input.addWidget(self.message_erreur, alignment=Qt.AlignmentFlag.AlignCenter)
            layout_conteneur_input.addWidget(self.message_valide, alignment=Qt.AlignmentFlag.AlignCenter)

            # --- layout bas (bouton retour, valider) --- #
            layout_bas = QHBoxLayout()

            bouton_retour = QPushButton("Retour")
            bouton_valider = QPushButton("Valider l'IP")
            
            layout_bas.addWidget(bouton_retour,alignment=Qt.AlignmentFlag.AlignLeft)
            layout_bas.addWidget(bouton_valider,alignment=Qt.AlignmentFlag.AlignRight)

            # --- composition de la fenêtre --- #
            layout_haut.addWidget(label_titre,alignment=Qt.AlignmentFlag.AlignCenter)
            layout_haut.addWidget(Widget_input)

            layout_principal.addLayout(layout_haut)
            layout_principal.addLayout(layout_bas)

            # --- appel des fonctions et autres fenêtres --- # 
            bouton_valider.clicked.connect(self.Verification_IP)
            bouton_retour.clicked.connect(self.appel_menuWindow)

    def appel_menuWindow(self):
    # --- ouverture de la fenêtre appelée et fermeture la fenêtre actuelle --- # 
            if self.menuW is None :
                self.menuW=menuWindow.Menu_Window()
                self.menuW.show() 
                self.close()
            else: 
                self.menuW.close()
                self.menuW = None
    def Verification_IP(self):
         self.message_valide.setText("")
         self.message_valide.setText("")
         ip_a_verifier=self.champ_ip.text()
         tool.validIP(self,ip_a_verifier)
            


if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("features/style.qss", "r") as fichier:
        app.setStyleSheet(fichier.read())

    fenetre = ValidationInput_Window()
    fenetre.show()
    sys.exit(app.exec())
