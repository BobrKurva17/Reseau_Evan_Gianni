import tool
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QDialog, QVBoxLayout, QFrame,QHBoxLayout
import CIDRWindow

class Menu_Window(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(250, 100, 1000, 750)
        self.setWindowTitle("Test")

        #initialisation de l'instance de la fenêtre CIDRWindows permet le retour en arriêre 
        self.CIDRW = None 
        # marges autour du panneau : laissent voir le fond
        layout_principal = QVBoxLayout(self)
        ##layout_principal.setContentsMargins(10, 20, 60, 40)

        # panneau central
        zone_boutons = QFrame()
        ##zone_boutons.setFixedWidth(600)
        zone_boutons.setObjectName("zone_boutons")

        # marges internes : le label et les boutons ne touchent pas les bords du panneau
        layout_boutons = QVBoxLayout(zone_boutons)
        layout_boutons.setContentsMargins(60, 30, 60, 30)
        layout_boutons.setSpacing(20)

        label_boutons = QLabel("Que souhaitez vous faire aujourd'hui ?")
        label_boutons.setObjectName("label_boutons")
        label_boutons.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.buttonCIDR = QPushButton("Tableau CIDR")
        self.buttonIP_Format_Valide = QPushButton("Vérifier votre IP")
        self.buttonClasse_IP = QPushButton("Déterminer la classe de votre IP")
        self.buttonMasque_IP = QPushButton("Déterminer le masque de classe de votre IP")
        self.buttonReseau_SR = QPushButton("Déterminer le réseau et sous-réseau")
        self.buttonMeme_reseau = QPushButton("Déterminer comment 2 machines communiquent")

        layout_boutons.addStretch()          # centre le contenu verticalement
        layout_boutons.addWidget(label_boutons)
        for bouton in (self.buttonCIDR, self.buttonIP_Format_Valide, self.buttonClasse_IP,
                       self.buttonMasque_IP, self.buttonReseau_SR, self.buttonMeme_reseau):
            layout_boutons.addWidget(bouton)
        layout_boutons.addStretch()

        layout_principal.addWidget(zone_boutons, alignment=Qt.AlignmentFlag.AlignCenter)
        # ligne du bas : bouton retour à gauche
        layout_bas = QHBoxLayout()
        self.bouton_retour = QPushButton("Retour")
        self.bouton_retour.setObjectName("bouton_retour")
        layout_bas.addWidget(self.bouton_retour)
        layout_bas.addStretch()          # pousse le bouton vers la gauche
        layout_principal.addLayout(layout_bas)

        self.buttonCIDR.clicked.connect(self.appel_CIDRWindow)

    def appel_CIDRWindow(self):
        #instanciation des autres fenêtres possibles 
        if self.CIDRW is None :
            self.CIDRW=CIDRWindow.CIDR_Window()
            self.CIDRW.show() 
            self.close()
        else: 
            self.CIDRW.close()
            self.CIDRW = None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("features/style.qss", "r") as fichier:
        app.setStyleSheet(fichier.read())

    fenetre = Menu_Window()
    fenetre.show()
    sys.exit(app.exec())